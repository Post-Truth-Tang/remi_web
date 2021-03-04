from position_operator.position_operator import PositionJsonOperator as TQZJsonOperator


class AccountModel:

    def __init__(self, account_name, account_jsonfile):
        self.account_name = account_name
        self.account_jsonfile = account_jsonfile


class AdministratorModel:

    @classmethod
    def __administrator_permission_jsonfile(cls):
        return "administrator_permission.json"

    @classmethod
    def __all_accounts_jsonfile(cls):
        return "all_accounts.json"


    @classmethod
    def administrator_name_list(cls):

        administrator_name_list = []
        for administrator in cls.administrator_models():
            administrator_name_list.append(administrator.administrator_name)

        return administrator_name_list


    # dictionary key string part
    @classmethod
    def __boss_key(cls):
        return "boss"

    @classmethod
    def __staff_key(cls):
        return "staff"

    @classmethod
    def __administrator_key(cls):
        return "administrator"

    @classmethod
    def __permission_key(cls):
        return "permission"

    @classmethod
    def __account_name_list_key(cls):
        return "account_name_list"


    def __reload_account_name_list(self, account_name_list):

        new_account_name_list = []
        account_jsonfile_dictionary = TQZJsonOperator.tqz_load_jsonfile(jsonfile=AdministratorModel.__all_accounts_jsonfile())
        if self.__permission == AdministratorModel.__boss_key():

            for account_name in account_jsonfile_dictionary.keys():
                new_account_name_list.append(account_name)

        elif self.__permission == AdministratorModel.__staff_key():

            for account_name in account_name_list:
                if account_name in account_jsonfile_dictionary.keys():
                    new_account_name_list.append(account_name)

        return new_account_name_list

    def __init__(self, administrator_dictionary):
        self.administrator_name = administrator_dictionary[AdministratorModel.__administrator_key()]
        self.__permission = administrator_dictionary[AdministratorModel.__permission_key()]

        # 两种情况 self.permission: boss、staff
        self.account_name_list = self.__reload_account_name_list(account_name_list=administrator_dictionary[AdministratorModel.__account_name_list_key()])


    @classmethod
    def administrator_is_exist(cls, administrator_name):

        is_exist = False
        for administrator in cls.administrator_models():
            if administrator.administrator_name == administrator_name:
                is_exist = True

        return is_exist

    def account_is_exist(self, account_name):
        return account_name in self.account_name_list


    @classmethod
    def administrator_models(cls):
        all_administrator_data = TQZJsonOperator.tqz_load_jsonfile(
            jsonfile=cls.__administrator_permission_jsonfile())

        administrator_models = []
        for administrator_dictionary in all_administrator_data:
            administrator_model = AdministratorModel(administrator_dictionary=administrator_dictionary)
            administrator_models.append(administrator_model)

        return administrator_models

    def account_models(self):
        account_jsonfile_dictionary = TQZJsonOperator.tqz_load_jsonfile(jsonfile=AdministratorModel.__all_accounts_jsonfile())

        account_models = []
        for account_name in self.account_name_list:
            if account_name in account_jsonfile_dictionary.keys():
                new_account_model = AccountModel(account_name=account_name, account_jsonfile=account_jsonfile_dictionary[account_name])
                account_models.append(new_account_model)

        return account_models

    @classmethod
    def administrator_model(cls, administrator_name):

        find_administrator_model = None
        for administrator_model in cls.administrator_models():
            if administrator_model.administrator_name == administrator_name:
                find_administrator_model = administrator_model

        return find_administrator_model

    def account_jsonfile(self, account_name):

        jsonfile = ""
        if self.account_is_exist(account_name=account_name):
            for account_model in self.account_models():
                if account_model.account_name == account_name:
                    jsonfile = account_model.account_jsonfile

        return jsonfile

    @classmethod
    def account_jsonfile_dictionary(cls, administrator_name):
        administrator_model = AdministratorModel.administrator_model(administrator_name=administrator_name)

        account_jsonfile_dictionary = {}
        if AdministratorModel.administrator_is_exist(administrator_name=administrator_name):
            account_models = administrator_model.account_models()
            for account_model in account_models:
                account_jsonfile_dictionary[account_model.account_name] = account_model.account_jsonfile

        return account_jsonfile_dictionary
