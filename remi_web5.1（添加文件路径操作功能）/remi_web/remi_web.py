from remi.server import App, start, Server
import remi.gui as gui
import time
from position_operator.position_operator import PositionJsonOperator as TQZJsonOperator
from position_operator.position_operator import ContractModel
from remi_model import AdministratorModel


class MainWeb(App):
    def __init__(self, *args):
        super(MainWeb, self).__init__(*args)

    def idle(self):
        # 每 60s 刷新一次
        if self.__is_refresh_time(now_time_second=time.localtime().tm_sec, interval_second=60) is True:
            self.__web_refresh(current_account_name=self.current_account_name)
            print(self.__time_now())

    def main(self):
        self.__window_load_data()

        return self.__add_child_widgets(current_account_name=self.current_account_name)

    # private part
    # - window load data / add child widgets -
    def __window_load_data(self):
        self.administrator_name_list = AdministratorModel.administrator_name_list()
        self.current_administrator_name = ""
        self.current_account_name = ""

    def __add_child_widgets(self, current_account_name):
        self.layout_width = '90%'
        self.window = gui.VBox(width='100%')  # 全屏

        # administrator_textInput 控件: 输入账户名
        self.administrator_textInput = self.__get_administrator_textInput()
        self.administrator_hint_label = gui.Label("", width=self.layout_width, height='10%')

        # account_textInput 控件: 输入账户名
        self.account_textInput = self.__get_account_textInput()
        self.account_name_list_hint_label = gui.Label("", width=self.layout_width, height='10%')

        # time_label 控件: 当前时间
        self.time_label = self.__get_time_label()

        # table控件: 账户对应的持仓数据
        self.table = self.__get_table(account_name=current_account_name)

        return self.__window_add_subviews(
            self.administrator_textInput,
            self.administrator_hint_label,

            self.account_textInput,
            self.account_name_list_hint_label,

            self.time_label,
            self.table,
            window=self.window
        )

    def __administrator_change(self, administrator_name):

        self.account_jsonfile_dictionary = AdministratorModel.account_jsonfile_dictionary(
            administrator_name=administrator_name
        )

        self.account_name_list = []
        [self.account_name_list.append(account_name) for account_name in self.account_jsonfile_dictionary.keys()]

        self.current_account_name = ""
        self.__web_refresh(current_account_name=self.current_account_name)

    # -- administrator text input widget part --
    def __get_administrator_textInput(self):
        administrator_textInput = gui.TextInput(
            single_line=True,
            hint="认证 管理员 (按 Enter 确认)",
            width=self.layout_width,
            height="10%"
        )

        administrator_textInput.onkeyup.do(callback=self.__administrator_textInput_onkeyup)

        return administrator_textInput

    def __administrator_textInput_onkeyup(self, widget, current_hint, last_presskey):
        self.current_administrator_name = current_hint
        self.current_account_name = ""
        self.administrator_hint_label.set_text(text="")
        self.account_textInput.set_text(text=self.current_account_name)
        self.account_name_list_hint_label.set_text(text="")

        self.__administrator_change(administrator_name="")  # 清空 当前管理员的 所有数据
        self.__web_refresh(current_account_name=self.current_account_name)

        if "13" == last_presskey:
            self.current_administrator_name = current_hint

            if self.current_administrator_name in self.administrator_name_list:
                self.administrator_hint_label.set_text(text="管理员 %s 认证成功;" % current_hint)
                self.current_administrator_name = current_hint
                self.__administrator_change(administrator_name=self.current_administrator_name)
            else:
                self.administrator_hint_label.set_text(text="不存在 %s 管理员;" % current_hint)


    # -- account text input widget part --
    def __get_account_textInput(self):
        account_textInput = gui.TextInput(
            single_line=True,
            hint="查询 账户 (按 Enter 确认)",
            width=self.layout_width,
            height="10%"
        )

        account_textInput.onkeyup.do(callback=self.__account_textInput_onkeyup)

        return account_textInput

    def __account_textInput_onkeyup(self, widget, current_hint, last_presskey):
        self.current_account_name = current_hint
        self.__web_refresh(current_account_name=self.current_account_name)

        if AdministratorModel.administrator_is_exist(administrator_name=self.current_administrator_name) is False:
            # --- 管理员 认证失败, 刷新 administrator_hint_label 和 account_name_list_hint_label ---
            self.administrator_hint_label.set_text(text="不存在 %s 管理员;" % self.administrator_textInput.get_text())
            self.account_name_list_hint_label.set_text(text="管理员 %s 认证失败;" % self.administrator_textInput.get_text())
            self.current_account_name = current_hint
            return
        elif AdministratorModel.administrator_is_exist(administrator_name=self.current_administrator_name) and 0 == len(self.account_name_list):
            # --- 管理员存在, 但是因为还没认证, 所以模型端还没拿到数据 ---
            self.account_name_list_hint_label.set_text(text="管理员 %s 尚未认证;" % self.administrator_textInput.get_text())
            self.current_account_name = current_hint
            return

        empty_account_list = []
        for account_name in self.account_name_list:
            if (current_hint is not "") and account_name.lower().startswith(current_hint.lower()):
                empty_account_list.append(account_name)

        empty_account_list_string = ', '.join(empty_account_list)

        if len(empty_account_list) is not 0:
            self.account_name_list_hint_label.set_text("账户查询结果: " + empty_account_list_string + ";")
        elif (len(empty_account_list) is 0) and (current_hint is ""):
            self.account_name_list_hint_label.set_text("")
        elif (len(empty_account_list) is 0) and (current_hint is not ""):
            self.account_name_list_hint_label.set_text("不存在 %s 账户;" % current_hint)

        if len(empty_account_list) != 0:
            current_hint = empty_account_list[0]

        if (last_presskey == "13") and (current_hint in self.account_name_list):
            # --- 按下回车时, 确认账户(current_hint)存在 ---
            self.current_account_name = current_hint
            self.account_textInput.set_text(self.current_account_name)
            self.account_name_list_hint_label.set_text("账户查询结果: " + self.current_account_name)
            self.__web_refresh(current_account_name=current_hint)
        elif (last_presskey == "13") and (current_hint not in self.account_name_list):
            # --- 按下回车时, 账户(current_hint)不存在 ---
            self.current_account_name = current_hint
            self.account_name_list_hint_label.set_text("不存在 %s 账户" % current_hint)
            self.__web_refresh(current_account_name=current_hint)


    # -- time label widget part --
    def __get_time_label(self):
        label_test = '更新时间: ' + self.__time_now()
        return gui.Label(label_test, width=self.layout_width, height='20%')

    @staticmethod
    def __time_now():
        return time.strftime("%Y/%m/%d  %H:%M:%S", time.localtime())


    # -- table widget part --
    def __get_table(self, account_name):
        content_data = self.__load_table_data(account_name=account_name)
        return gui.Table.new_from_list(content=content_data, width=self.layout_width, fill_title=True)  # fill_title: True代表第一行是蓝色, False代表表格内容全部同色

    def __load_table_data(self, account_name):
        title_cell = ("合约", "当前持仓", "入场价", "目标持仓")
        table_data = [title_cell]

        if AdministratorModel.administrator_is_exist(administrator_name=self.current_administrator_name) is False:
            return table_data
        elif account_name not in self.account_jsonfile_dictionary.keys():
            return table_data

        jsonfile = self.account_jsonfile_dictionary[account_name]
        account_data_dic = TQZJsonOperator.tqz_load_jsonfile(jsonfile=jsonfile)

        contract_models = ContractModel.dictionary_to_models(data_dictionary=account_data_dic)
        for contract_model in contract_models:
            empty_cell = [
                str(contract_model.name),
                str(contract_model.position_model.lots),
                str(contract_model.position_model.entry_price),
                # str(contract_model.position_model.target_position),
            ]

            target_position = contract_model.position_model.target_position
            if (target_position is None) or (0 == target_position):
                empty_cell.append("0")

            table_data.append(tuple(empty_cell))

        return table_data


    # -- web refresh part --
    @staticmethod
    def __is_refresh_time(now_time_second, interval_second):
        """
            判断当前时间, 是否应该刷新数据(table_data、table控件、time_label_控件)
        :param now_time_second: 当前时间的 秒数
        :param interval_second: 刷新一次所用时间
        :return: 当前秒数是否应该刷新
        """

        if now_time_second % interval_second is 0:
            should_refresh = True
        else:
            should_refresh = False

        return should_refresh

    def __web_refresh(self, current_account_name):
        self.administrator_textInput.set_text(text=self.current_administrator_name)
        self.account_textInput.set_text(text=current_account_name)
        self.time_label.set_text(text='更新时间: ' + self.__time_now())

        self.window.remove_child(self.table)
        table_content = self.__load_table_data(account_name=current_account_name)
        self.table = gui.Table.new_from_list(content=table_content, width=self.layout_width, fill_title=True)
        self.__window_add_subviews(self.table, window=self.window)

    @staticmethod
    def __window_add_subviews(*subviews, window):
        [window.append(subview) for subview in subviews]
        return window


if __name__ == '__main__':
    app = Server(gui_class=MainWeb, update_interval=1, port=8876)  # 参数 update_interval: 程序每1s调用一次 idel() 函数;
