from py12306.log.base import BaseLog
from py12306.config import *
from py12306.helpers.func import *


@singleton
class CommonLog(BaseLog):
    # 这里如果不声明，会出现重复打印，目前不知道什么原因
    logs = []
    thread_logs = {}
    quick_log = []

    MESSAGE_12306_IS_CLOSED = '当前时间: {}     |       12306 休息时间，程序将在明天早上 6 点自动运行'
    MESSAGE_RETRY_AUTH_CODE = '{} 秒后重新获取验证码'

    MESSAGE_EMPTY_APP_CODE = '无法发送语音消息，未填写验证码接口 appcode'
    MESSAGE_VOICE_API_FORBID = '语音消息发送失败，请检查 appcode 是否填写正确或 套餐余额是否充足'
    MESSAGE_VOICE_API_SEND_FAIL = '语音消息发送失败，错误原因 {}'
    MESSAGE_VOICE_API_SEND_SUCCESS = '语音消息发送成功! 接口返回信息 {} '

    MESSAGE_CHECK_AUTO_CODE_FAIL = '请配置打码账号的账号密码'
    MESSAGE_CHECK_EMPTY_USER_ACCOUNT = '请配置 12306 账号密码'

    MESSAGE_TEST_SEND_VOICE_CODE = '正在测试发送语音验证码...'
    MESSAGE_TEST_SEND_EMAIL = '正在测试发送邮件...'
    MESSAGE_TEST_SEND_DINGTALK = '正在测试发送钉钉消息...'
    MESSAGE_TEST_SEND_TELEGRAM = '正在测试推送到Telegram...'
    MESSAGE_TEST_SEND_SERVER_CHAN = '正在测试发送ServerChan消息...'
    MESSAGE_TEST_SEND_PUSH_BEAR = '正在测试发送PushBear消息...'
    MESSAGE_TEST_SEND_PUSH_BARK = '正在测试发送Bark消息...'

    MESSAGE_CONFIG_FILE_DID_CHANGED = '配置文件已修改，正在重新加载中\n'
    MESSAGE_API_RESPONSE_CAN_NOT_BE_HANDLE = '接口返回错误'

    MESSAGE_SEND_EMAIL_SUCCESS = '邮件发送成功，请检查收件箱'
    MESSAGE_SEND_EMAIL_FAIL = '邮件发送失败，请手动检查配置，错误原因 {}'

    MESSAGE_SEND_EMAIL_WITH_QRCODE_SUCCESS = '二维码邮件发送成功，请检查收件箱扫描登陆'

    MESSAGE_SEND_TELEGRAM_SUCCESS = 'Telegram推送成功'
    MESSAGE_SEND_TELEGRAM_FAIL = 'Telegram推送失败，错误原因 {}'

    MESSAGE_SEND_SERVER_CHAN_SUCCESS = '发送成功，请检查微信'
    MESSAGE_SEND_SERVER_CHAN_FAIL = 'ServerChan发送失败，请检查KEY'

    MESSAGE_SEND_PUSH_BEAR_SUCCESS = '发送成功，请检查微信'
    MESSAGE_SEND_PUSH_BEAR_FAIL = 'PushBear发送失败，请检查KEY'

    MESSAGE_SEND_BARK_SUCCESS = 'Bark推送成功'
    MESSAGE_SEND_BARK_FAIL = 'Bark推送失败，错误原因 {}'

    MESSAGE_OUTPUT_TO_FILE_IS_UN_ENABLE = '请先打开配置项中的：OUT_PUT_LOG_TO_FILE_ENABLED ( 输出到文件 )'

    MESSAGE_GET_RESPONSE_FROM_FREE_AUTO_CODE = '从免费打码获取结果失败'

    MESSAGE_RESPONSE_EMPTY_ERROR = '网络错误'

    MESSAGE_CDN_START_TO_CHECK = '正在筛选 {} 个 CDN...'
    MESSAGE_CDN_START_TO_RECHECK = '正在重新筛选 {} 个 CDN...当前时间 {}\n'
    MESSAGE_CDN_RESTORE_SUCCESS = 'CDN 恢复成功，上次检测 {}\n'
    MESSAGE_CDN_CHECKED_SUCCESS = '# CDN 检测完成，可用 CDN {} #\n'
    MESSAGE_CDN_CLOSED = '# CDN 已关闭 #'

    def __init__(self):
        super().__init__()
        self.init_data()

    def init_data(self):
        pass

    @classmethod
    def print_welcome(cls):
        self = cls()
        self.add_quick_log('######## 🚅Helper 12306，本程序为开源工具，请勿用于商业用途 ########')
        if Const.IS_TEST:
            self.add_quick_log()
            self.add_quick_log('当前为测试模式，程序运行完成后自动结束')
        if not Const.IS_TEST and Config().OUT_PUT_LOG_TO_FILE_ENABLED:
            self.add_quick_log()
            self.add_quick_log('日志已输出到文件中: {}'.format(Config().OUT_PUT_LOG_TO_FILE_PATH))
        if Config().WEB_ENABLE:
            self.add_quick_log()
            self.add_quick_log('WEB 管理页面已开启，请访问 主机地址 + 端口 {} 进行查看'.format(Config().WEB_PORT))

        self.add_quick_log()
        self.flush(file=False, publish=False)
        return self

    @classmethod
    def print_configs(cls):
        # 打印配置
        self = cls()
        enable = '已开启'
        disable = '未开启'
        self.add_quick_log('**** 当前配置 ****')
        self.add_quick_log('多线程查询: {}'.format(get_true_false_text(Config().QUERY_JOB_THREAD_ENABLED, enable, disable)))
        self.add_quick_log('CDN 状态: {}'.format(get_true_false_text(Config().CDN_ENABLED, enable, disable))).flush()
        self.add_quick_log('通知状态:')
        if Config().NOTIFICATION_BY_VOICE_CODE:
            self.add_quick_log(
                '语音验证码: {}'.format(get_true_false_text(Config().NOTIFICATION_BY_VOICE_CODE, enable, disable)))
        if Config().EMAIL_ENABLED:
            self.add_quick_log('邮件通知: {}'.format(get_true_false_text(Config().EMAIL_ENABLED, enable, disable)))
        if Config().DINGTALK_ENABLED:
            self.add_quick_log('钉钉通知: {}'.format(get_true_false_text(Config().DINGTALK_ENABLED, enable, disable)))
        if Config().TELEGRAM_ENABLED:
            self.add_quick_log('Telegram通知: {}'.format(get_true_false_text(Config().TELEGRAM_ENABLED, enable, disable)))
        if Config().SERVERCHAN_ENABLED:
            self.add_quick_log(
                'ServerChan通知: {}'.format(get_true_false_text(Config().SERVERCHAN_ENABLED, enable, disable)))
        if Config().BARK_ENABLED:
            self.add_quick_log('Bark通知: {}'.format(get_true_false_text(Config().BARK_ENABLED, enable, disable)))
        if Config().PUSHBEAR_ENABLED:
            self.add_quick_log(
                'PushBear通知: {}'.format(get_true_false_text(Config().PUSHBEAR_ENABLED, enable, disable)))
        self.add_quick_log().flush(sep='\t\t')
        self.add_quick_log('查询间隔: {} 秒'.format(Config().QUERY_INTERVAL))
        self.add_quick_log('用户心跳检测间隔: {} 秒'.format(Config().USER_HEARTBEAT_INTERVAL))
        self.add_quick_log('WEB 管理页面: {}'.format(get_true_false_text(Config().WEB_ENABLE, enable, disable)))
        if Config().is_cluster_enabled():
            from py12306.cluster.cluster import Cluster
            self.add_quick_log('分布式查询: {}'.format(get_true_false_text(Config().is_cluster_enabled(), enable, enable)))
            self.add_quick_log('节点名称: {}'.format(Cluster().node_name))
            self.add_quick_log('节点是否主节点: {}'.format(get_true_false_text(Config().is_master(), '是', '否')))
            self.add_quick_log(
                '子节点提升为主节点: {}'.format(get_true_false_text(Config().NODE_SLAVE_CAN_BE_MASTER, enable, disable)))
        self.add_quick_log()
        self.flush()
        return self

    @classmethod
    def print_test_complete(cls):
        self = cls()
        self.add_quick_log('# 测试完成，请检查输出是否正确 #')
        self.flush(publish=False)
        return self

    @classmethod
    def print_auto_code_fail(cls, reason):
        self = cls()
        self.add_quick_log('打码失败: 错误原因 {reason}'.format(reason=reason))
        self.flush()
        return self

    @classmethod
    def print_auth_code_info(cls, reason):
        self = cls()
        self.add_quick_log('打码信息: {reason}'.format(reason=reason))
        self.flush()
        return self
