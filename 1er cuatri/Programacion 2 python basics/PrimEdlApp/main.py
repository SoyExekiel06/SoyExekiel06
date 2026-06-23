from data.DataHelperFactory import get_data_helper
from presentation.Usuarios import App
 
if __name__ == "__main__":
    data_helper = get_data_helper()
    App(data_helper).menu_acceso()