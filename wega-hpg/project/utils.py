menu = [
    {'title': "Главная",     'url_name': 'home'},
    {'title': "Калькулятор", 'url_name': 'profile_index'},
    # {'title': "Настройки",   'url_name': ''},
    {'title': "Wiki",   'url_name': 'wiki_pages'},
    
    # {'title': "Помощь", 'url_name': ''},
    # {'title': "О проекте", 'url_name': ''},
]

menu_all = [
    {'title': "Главная",     'url_name': 'home'},
    {'title': "Wiki", 'url_name': 'wiki_pages'},
]


class DataMixin:
    paginate_by = 2
    @classmethod
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        context['menu'] = user_menu
        context['menu_all'] = menu_all
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
 

