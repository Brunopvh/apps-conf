#!/usr/bin/env python3
#

"""
  Biblioteca facilitar a instalação de aplicativos em sistemas 
Linux e Windows.

"""

__version__ = '0.2'
__author__ = 'Bruno Chaves'
__repo__ = 'https://gitlab.com/bschaves/apps-conf'
__online_file__ = 'https://gitlab.com/bschaves/apps-conf/-/archive/main/apps-conf-main.zip'

from platform import system
from shutil import copyfile
import json
from tempfile import NamedTemporaryFile, TemporaryDirectory
import os.path
from os import (
    makedirs,
    geteuid,
    environ,
    remove,
)

from pathlib import Path

HOME = os.path.abspath(Path().home())
KERNEL_TYPE = system()
del  system


def mkdir(path: str) -> bool:
    """Função para criar um diretório."""
    if path is None:
        return False

    if os.path.exists(path):
        return True
        
    try:
        makedirs(path)
    except Exception as e:
        print(__name__, e)
        return False
    else:
        return True


def get_abspath(path: str) -> str:
    """Retorna o caminho absoluto de um arquivo ou diretório."""
    return os.path.abspath(path)


def touch(file) -> bool:
    try:
        Path(file).touch()
    except:
        return False
    else:
        return True




class FilePath(object):
    """
       Classe para trabalhar com um arquivo, e obter algumas informações como:
    path()      - Caminho absoluto.
    exists()    - Verificar se o arquivo existe.
    name()      - Retorna o nome do arquivo, sem a extensão. 
    dirname()   - Retorna o diretório PAI do arquivo.
    basename()  - Retorna o nome do arquivo com a extensão.
    extension() - Retorna a extensão do arquivo, com base no nome.
    """
    def __init__(self, file: str) -> None:
        super().__init__()
        self.file = file

    def path(self) -> str:
        """Retorna o caminho absoluto de um arquivo"""
        return get_abspath(self.file)

    def exists(self) -> bool:
        try:
            if os.path.exists(self.path()):
                return True
        except:
            return False

    def name(self) -> str:
        """
           Retorna o nome do arquivo sem a extensão, e sem o caminho absoluto.
        Ex:
           /path/to/file_name.pdf

        name() -> file_name
        """
        if self.extension() is None:
            return self.basename()
        return self.basename().replace(self.extension(), "")
    
    def dirname(self) -> str:
        """
           Retorna o caminho absoluto do diretório pai do arquivo.
        """
        return os.path.dirname(self.path())

    def basename(self) -> str:
        """
           Retorna o nome do arquivo com a extensão, sem o caminho absoluto.
        Ex:
           /path/to/file_name.pdf

        basename() -> file_name.pdf
        """
        return os.path.basename(self.path())
        
    def drive(self):
        return Path(self.path()).drive

    def extension(self) -> str:
        """Retorna a extensão do arquivo baseado no nome"""
        _ext = os.path.splitext(self.path())[1]
        if _ext == '': 
            return None
        return _ext
    
    def touch(self) -> None:
        Path(self.path()).touch()

    def delete(self) -> None:
        """Deleta o arquivo"""
        try:
            remove(self.path())
        except Exception as e:
            print(__class__.__name__, e)



class FileReader(object):
    """
       Classe para ler e escrever linhas em arquivos de texto

    get_lines() - Retorna as linhas de um arquivo em forma de lista.
    write_lines(list) - Recebe uma lista, e grava os dados da lista no arquivo.
    """

    def __init__(self, file_path: FilePath) -> None:
        super().__init__()
        self.file_path: FilePath = file_path

    def get_lines(self) -> list:
        """Retorna uma lista com as linhas do arquivo de texto."""
        lines = []
        try:
            with open(self.file_path.path(), 'rt') as file:
                lines = file.readlines()

        except Exception as e:
            print(__class__.__name__, e)
            return lines
        else:
            return lines

    def write_lines(self, lines: list) -> None:
        """
           Sobreescrever um arquivo, gravando o conteúdo de lines no arquivo.
        Todos os dados existentes serão perdidos. Quebras de linha '\n' são 
        inseridas automáticamente no fim de cada linha.
        """
        if not isinstance(lines, list):
            print(__class__.__name__, "ERRO ... lines precisa ser do tipo lista")
            return

        try:
            with open(self.file_path.path(), 'w') as file:
                for line in lines:
                    file.write(f'{line}\n')
        except Exception as e:
            print(__class__.__name__, e)

    def append_lines(self, lines: list) -> None:
        """Adiciona o conteúdo de lines no fim do arquivo de texto"""
        if not isinstance(lines, list):
            print(__class__.__name__, "ERRO ... lines precisa ser do tipo lista")
            return

        try:
            with open(self.file_path.path(), 'a') as file:
                for line in lines:
                    file.write(f'{line}\n')
        except Exception as e:
            print(__class__.__name__, e)

    def is_text(self, text: str) -> bool:
        """Verifica se text existe no arquivo de texto"""
        if len(self.find_text(text)) > 0:
            return True
        return False
    
    def find_text(self, text: str, *, max_count: int=0, ignore_case:bool=False) -> list:
        """
            Retorna uma lista com todas as ocorrências de text nas linhas do arquivo.
        max_cout = Máximo de ocorrências a buscar no arquivo.
        ignore_case = Ignora o case sensitive.
        """
        _lines = self.get_lines()
        _lst = []
        if _lines == []:
            return []

        for line in _lines:
            if ignore_case:
                if text.lower() in line.lower():
                    _lst.append(line)
            else:
                if text in line:
                    _lst.append(line)

            if (max_count > 0) and (len(_lst) == max_count):
                break
           
        return _lst

        

class FileJson(object):
    """
       Classe com as funcionalidades:
    - Ler um arquivo json e retornar o conteúdo em forma de dicionário.

    - Sobreescrever/Criar um arquivo json apartir de um dicionário. 

    - Alterar/Adicionar o conteúdo de uma chave.

    - Alterar/Adicionar uma chave.

    """
    def __init__(self, file_path_json: FilePath):
        super().__init__()
        self.file_path_json: FilePath = file_path_json

    def write_lines(self, new_lines: dict):
        """
        Apaga o conteúdo do arquivo .json, e escreve os dados 'new_lines' no arquivo.
        """

        if not isinstance(new_lines, dict):
            #print(f'{__class__.__name__} ERRO')
            raise Exception(f'{__class__.__name__} ERRO ... tipo de dados incorreto ... {new_lines}')
            return

        try:
            with open(self.file_path_json.path(), 'w', encoding='utf8') as jfile:
                json.dump(new_lines, jfile, ensure_ascii=False, sort_keys=True, indent=4)
        except Exception as e:
            #print(__class__.__name__, e)
            raise Exception(f'{__class__.__name__} {e}')

    def lines_to_dict(self) -> dict:
        """
        Ler o conteúdo do arquivo .json e retornar as linhas em forma de um dicionário
        """
        try:
            with open(self.file_path_json.path(), 'rt', encoding='utf8') as jfile:
                content = json.load(jfile)
        except Exception as e:
            print(__class__.__name__, e)
            return {}
        else:
            return content

    def update_key(self, new_key: str, value: str):
        """
          Altera/Cria a chave 'new_key' com o valor 'value'

        Se new_key já existir, será modificada, se não será alterada.
        """
        content = self.lines_to_dict()

        if not new_key in content.keys():
            content.update({new_key: value})
        else:
            content[new_key] = value

        self.write_lines(content)

    def is_key(self, key: str) -> bool:
        """Verifica se uma chave/key existe no json"""
        _keys = self.lines_to_dict().keys()

        for json_key in self.lines_to_dict().keys():
            if json_key == key:
                return True
                break
        return False

    def get_lines(self):
        return json.dumps(self.lines_to_dict(), indent=4, ensure_ascii=False)
        


class PathUserDirs(object):
    """Diretórios para cache, configurações, libs, binários entre outros."""
    def __init__(self, *, type_root: bool = False) -> None:
        super().__init__()
        self.type_root: bool = type_root
        self.__temp_dir = None
        self.__temp_file = None
    
    @property
    def type_root(self) -> bool:
        return self._type_root

    @type_root.setter
    def type_root(self, new_type_root) -> None:
        """Proteger atribuições para type_root."""
        if geteuid() == 0:
            self._type_root = True
            return
        if not isinstance(new_type_root, bool):
            self._type_root = False
            return
        self._type_root = new_type_root

    def getDirs(self) -> dict:
        """
           Retorna todos os diretórios e arquivos de configuração em forma de um dicionário.
        """
        pass

    def setDirs(self) -> None:
        """Atribuir os diretórios para o root ou para user"""
        pass

    def tempDir(self, *, create=False) -> str:
        """
           Retorna um diretório temporário.
        """
        if self.__temp_dir is None:
            self.__temp_dir = TemporaryDirectory().name
        if create:
            mkdir(self.__temp_dir)

        return self.__temp_dir

    def tempFile(self, create=False) -> None:
        if self.__temp_file is None:
            self.__temp_file = NamedTemporaryFile(delete=True).name
        if create:
            touch(self.__temp_file)

        return self.__temp_file

    def dirHome(self) -> str:
        pass

    def getDirIcons(self, resol: str) -> str:
        """Retorna um diretório para guardar icones."""
        pass

    def showDirs(self):
        """Mostra os diretórios de configuração no STDOUT."""
        pass   

    def fileBashRc(self) -> str:
        pass

    def dirGnupg(self) -> str:
        pass
        
    def dirDownloads(self) -> str:
        """Retorna o diretório Downloads do Usuário"""
        pass

    def dirOptional(self) -> str:
        pass

    def dirConfig(self) -> str:
        pass

    def dirCache(self) -> str:
        pass

    def dirThemes(self) -> str:
        pass

    def dirDesktopEntry(self) -> str:
        pass

    def dirIcons(self) -> str:
        pass

    def dirLib(self) -> str:
        pass

    def dirBin(self) -> str:
        pass

    def getDirIcons(self, resol: str) -> str:
        pass



class ConfDirsLinux(PathUserDirs):
    """
      Classe para trabalhar com o caminho absoluto de diretório
    para instalação de aplicativos em sistemas Linux.
    """
    def __init__(self, *, type_root: bool=False) -> None:
        
        # type_root: se for False esta classe irá trabalhar com as 
        # configurações de usuário padrão, se for True, irá trabalhar
        # com as configurações do usuário root.
        if geteuid() == 0:
            # Se o id do usuário for root type_root será True automáticamente.
            super().__init__(type_root=True)
        else:
            super().__init__(type_root=type_root)
        self.setDirs()

    @property
    def type_root(self) -> bool:
        return self._type_root

    @type_root.setter
    def type_root(self, new_type_root) -> None:
        if geteuid() == 0:
            self._type_root = True
        else:
            self._type_root = new_type_root
        
    def setDirs(self):
        pass

    def dirHome(self) -> str:
        """Retorna a HOME do usuário."""
        if self.type_root:
            return '/root'
        return os.path.abspath(Path().home())

    def fileBashRc(self) -> str:
        if self.type_root:
            return '/etc/bash.bashrc'
        return get_abspath(os.path.join(self.dirHome(), '.bashrc'))

    def dirGnupg(self) -> str:
        if self.type_root:
            return '/root/.gnupg'
        return get_abspath(os.path.join(self.dirHome(), '.gnupg'))
        
    def dirDownloads(self) -> str:
        """Retorna o diretório Downloads do Usuário"""
        if self.type_root:
            return '/root/Downloads'
        return get_abspath(os.path.join(self.dirHome(), 'Downloads'))

    def dirOptional(self) -> str:
        if self.type_root:
            return '/opt'
        return get_abspath(os.path.join(self.dirHome(), '.local', 'opt'))

    def dirConfig(self) -> str:
        if self.type_root:
            return '/etc'
        return get_abspath(os.path.join(self.dirHome(), '.config'))

    def dirCache(self) -> str:
        if self.type_root:
            return '/var/cache'
        return get_abspath(os.path.join(self.dirHome(), '.cache'))

    def dirThemes(self) -> str:
        if self.type_root:
            return '/usr/share/themes'
        return get_abspath(os.path.join(self.dirHome(), '.themes'))

    def dirDesktopEntry(self) -> str:
        if self.type_root:
            return '/usr/share/applications'
        return get_abspath(os.path.join(self.dirHome(), '.local', 'share', 'applications'))

    def dirIcons(self) -> str:
        if self.type_root:
            return '/usr/share/icons/hicolor/128x128/apps'
        return get_abspath(os.path.join(self.dirHome(), '.local', 'share', 'icons', '128x128'))

    def dirLib(self) -> str:
        if self.type_root:
            return '/usr/local/lib'
        return get_abspath(os.path.join(self.dirHome(), '.local', 'lib'))

    def dirBin(self) -> str:
        if self.type_root:
            return '/usr/local/bin'
        return get_abspath(os.path.join(self.dirHome(), '.local', 'bin')) 

    def getDirIcons(self, resol: str) -> str:
        """
           resol = Resolução (96x96, 128x128, 256x256, ...)
        Retorna um caminho em: 
           /usr/share/icons/hicolor/resol/apps OU
           ~/.local/share/icons/hicolor/resol/apps
        """
        if self.type_root:
            _path = self.dirIcons().split('/')
            _path[5] = resol
            return "/".join(_path)
        else:
            _path = self.dirIcons().split('/')
            _path[6] = resol
            return "/".join(_path)

    def getDirs(self) -> dict:
        
        return {
            'HOME': self.dirHome(),
            'DIR_DOWNLOADS': self.dirDownloads(),
            'DIR_BIN': self.dirBin(),
            'DIR_LIB': self.dirLib(),
            'DIR_ICONS': self.dirIcons(),
            'DIR_DESKTOP_ENTRY': self.dirDesktopEntry(),
            'DIR_THEMES': self.dirThemes(),
            'DIR_OPTIONAL': self.dirOptional(),
            'DIR_CACHE': self.dirCache(),
            'DIR_CONFIG': self.dirConfig(),
            'FILE_BASHRC': self.fileBashRc(),
        }

       

class ConfDirsWindows(PathUserDirs):
    """
    Esta classe tem como atributos, diretórios comumente usados por programas no sitema Windows.
    """
    def __init__(self, *, type_root: bool=False):
        super().__init__(type_root)

    def dirHome(self) -> str:
        """Retorna a HOME do usuário."""
        return os.path.abspath(Path().home())
        
    def dirGnupg(self) -> str:
        return get_abspath(os.path.join(self.dirHome(), '.gnupg'))
        
    def dirOptional(self) -> str:
        return get_abspath(os.path.join(self.dirHome(), 'AppData', 'Local', 'Programs'))
        
    def dirBin(self) -> str:
        return get_abspath(os.path.join(self.dirHome(), 'AppData', 'Local', 'Programs'))

    def dirLib(self) -> str:
        return super().dirLib()

    def dirDownloads(self) -> str:
        return get_abspath(os.path.join(self.dirHome(), 'Downloads'))

    def dirConfig(self) -> str:
        return get_abspath(os.path.join(self.dirHome(), 'AppData', 'Roaming'))

    def dirCache(self) -> str:
        return get_abspath(os.path.join(self.dirHome(), 'AppData', 'LocalLow'))

    def getDirs(self) -> dict:
        """
          Retorna um dicionário com diretórios.

          :rtype dict
        """
        return {
            'HOME': self.dirHome(),
            'DIR_CACHE': self.dirCache(),
            'DIR_CONFIG': self.dirConfig(),
            'DIR_BIN': self.dirBin(),
            'DIR_OPTIONAL': self.dirOptional(),
            'DIR_GNUPG': self.dirGnupg(),
            }



class ConfDirs(object):
    def __init__(self, *, type_root:bool=False) -> None:
        #super().__init__(type_root=type_root) 
        self.type_root = type_root
       
    @property
    def type_root(self) -> bool:
        return self._type_root

    @type_root.setter
    def type_root(self, new_type_root) -> None:
        if geteuid() == 0:
            self._type_root = True
        else:
            self._type_root = new_type_root
        
        if KERNEL_TYPE == 'Windows':
            self.__conf_user_dirs: ConfDirsWindows = ConfDirsWindows(type_root=self._type_root)
        elif KERNEL_TYPE == 'Linux':
            self.__conf_user_dirs: ConfDirsLinux = ConfDirsLinux(type_root=self._type_root)
        else:
            exit(1)

        self.__conf_user_dirs.setDirs()

    def tempDir(self, *, create:bool=False) -> str:
        """
           Retorna um diretório temporário.
        """
        return self.__conf_user_dirs.tempDir(create=create)

    def tempFile(self, create: bool=False) -> None:
        """Retorna um arquivo temporário"""
        return self.__conf_user_dirs.tempFile(create=create)

    def dirHome(self) -> str:
        """Retorna o diretório Home do usuário."""
        return self.__conf_user_dirs.dirHome()

    def dirDownloads(self) -> str:
        """Retorna o diretório downloads do usuário."""
        return self.__conf_user_dirs.dirDownloads()

    def dirBin(self) -> str:
        return self.__conf_user_dirs.dirBin()

    def dirOptional(self) -> str:
        return self.__conf_user_dirs.dirOptional()

    def dirCache(self) -> str:
        return self.__conf_user_dirs.dirCache()

    def dirConfig(self) -> str:
        return self.__conf_user_dirs.dirConfig()

    def dirDesktopEntry(self) -> str:
        if KERNEL_TYPE != 'Linux':
            return None
        return self.__conf_user_dirs.dirDesktopEntry()

    def dirThemes(self) -> str:
        if KERNEL_TYPE != 'Linux':
            return None
        return self.__conf_user_dirs.dirThemes()

    def dirLib(self) -> str:
        if KERNEL_TYPE != 'Linux':
            return None
        return self.__conf_user_dirs.dirLib()

    def dirIcons(self) -> str:
        if KERNEL_TYPE != 'Linux':
            return None
        return self.__conf_user_dirs.dirIcons()

    def fileBashRc(self) -> str:
        if KERNEL_TYPE != 'Linux':
            return None
        return self.__conf_user_dirs.fileBashRc()

    def getDirIcons(self, resol: str):
        return self.__conf_user_dirs.getDirIcons(resol)

    def getDirs(self) -> dict:
        return self.__conf_user_dirs.getDirs()
        

    def dirsJson(self):
        """
           Retorna os valores em formato Json.
        
        self.get_dirs(): dict -> self.get_dirs(): json
        """
        return json.dumps(self.getDirs(), indent=4)

    def showDirs(self):
        _dirs = self.getDirs()
        for _key in _dirs:
            print(f'{_key}'.ljust(19), end=' ')
            print(_dirs[_key])
    
    def setDirs(self):
        self.__conf_user_dirs.setDirs()
        

#===============================================================#

# Função para ser usada em sistemas Linux.
def add_home_in_path() -> bool:
    '''
       Configurar o arquivo .bashrc do usuário para inserir o diretório ~/.local/bin
    na variável de ambiente $PATH. 
    
       Essa configuração será abortada caso ~/.local/bin já exista em ~/.bashrc ou exista na variável $PATH.
    '''
    if KERNEL_TYPE != 'Linux':
        print(f'{__name__} ERRO ... sistema operacional não suportado.')
        return False

    if geteuid() == 0:
        print(f'{__name__} ERRO ... você não pode ser o "root."')
        return False
    
    
    confUserDirs: ConfDirs = ConfDirs(type_root=False)

    # Verificar se ~/.local/bin já está no PATH do usuário atual.
    # os.environ
    user_local_path = environ['PATH']
    
    for _dir in user_local_path.split(':'):
        if _dir == confUserDirs.dirBin():
            return True
            break

    file_bashrc_backup = confUserDirs.fileBashRc() + '.bak'
    if not os.path.isfile(file_bashrc_backup):
        print(f'Criando backup do arquivo {confUserDirs.fileBashRc()}')
        copyfile(confUserDirs.fileBashRc(), file_bashrc_backup)

    file_bash: FilePath = FilePath(confUserDirs.fileBashRc()) 
    file_reader: FileReader = FileReader(file_bash)
    content: list = file_reader.get_lines()

    import re
    RegExp = re.compile(r'{}.*{}'.format('^export PATH=', confUserDirs.dirBin()))
    for line in content:
        if (RegExp.findall(line) != []): # O arquivo já foi configurado anteriormente.
            print(f'add_home_in_path(): arquivo {confUserDirs.fileBashRc()} já configurado.')
            return True
            break

    # Inserir ~/.local/bin no arquivo ~/.bashrc
    NewUserPath = f'export PATH={confUserDirs.dirBin()}:{user_local_path}'
    content.append(NewUserPath)

    # Escrever a nova lista no arquivo ~/.bashrc
    file_reader.write_lines(content)

    del confUserDirs
    del file_reader
    del file_bash
    del content
    del re

    return True


class AppDirs(object):
    def __init__(self, *, type_root:bool=False, appname: str) -> None:
        super().__init__()
        # Appname é o nome do aplicativo que irá usar esta classe
        # para obter informações de arquivos e diretórios de configuração.
        self.appname = appname
        self.type_root = type_root
        
        if self.config_dirs is None:
            print(f'{__class__.__name__} ERRO ... sistema operacional não suportado.')
            exit(1)

    @property
    def appname(self) -> str:
        return self._appname

    @appname.setter
    def appname(self, new_appname: str) -> None:
        self._appname = new_appname

    @property
    def type_root(self) -> bool:
        return self._type_root

    @type_root.setter
    def type_root(self, new_type_root: bool) -> None:
        if geteuid() == 0:
            self._type_root = True
        else:
            self._type_root = new_type_root
        
        self.config_dirs: ConfDirs = ConfDirs(type_root=self._type_root)
        self.config_dirs.setDirs()

    def get_dirs(self):
        return {
            'APP_DIR': self.appdir(),
            'APP_DIR_CACHE': self.dircache(),
            'APP_DIR_CONFIG': self.dirconfig(),
            'APP_DIR_LIB': self.dirlib(),
        }

    def dirlib(self) -> str:
        return get_abspath(os.path.join(self.config_dirs.dirLib(), self.appname))

    def dircache(self) -> str:
        return get_abspath(os.path.join(self.config_dirs.dirCache(), self.appname))

    def dirconfig(self) -> str:
        return get_abspath(os.path.join(self.config_dirs.dirConfig(), self.appname))

    def appdir(self) -> str:
        return get_abspath(os.path.join(self.config_dirs.dirOptional(), self.appname))

    def fileconf(self) -> str:
        """Retorna o caminho de um arquivo .json no diretório de configuração"""
        return get_abspath(os.path.join(self.dirconfig(), f'{self.appname}.json'))

    def fileConfPath(self) -> FilePath:
        """Retorna uma instância de FilePath para o arquivo self.fileconf()"""
        return FilePath(self.fileconf())

    def script(self) -> str:
        return get_abspath(os.path.join(self.config_dirs.dirBin(), self.appname))

    def scriptPath(self) -> FilePath:
        """Retorna uma instância de FilePath para o arquivo self.script()"""
        return FilePath(self.script())

    def icon(self, file_icon: str) -> str:
        """
          Recebe o nome de um arquivo (.png, .jpg, ,svg ...)
        Retorna o caminho onde o icone deve estar no sistema.
        """
        return get_abspath(os.path.join(self.config_dirs.dirIcons(), file_icon))

    def get_dir_icons(self, resol: str) -> str:
        return self.config_dirs.getDirIcons(resol)

    def get_temp_dir(self, *, create=False) -> str:
        """
           Retorna um diretório temporário.
        """
        return self.config_dirs.tempDir(create=create)

    def get_temp_file(self, create=False) -> None:
        """Retorna um arquivo temporário."""
        return self.config_dirs.tempFile(create=create)

    def desktop_entry(self, file_desktop) -> str:
        """
        A extensão .desktop é adicionada automáticamente.

        Retorna o caminho completo do arquivo .desktop.
        """
        if file_desktop[-8:] != '.desktop':
            file_desktop += '.desktop'

        return get_abspath(os.path.join(self.config_dirs.dirDesktopEntry(), file_desktop))

    def desktopEntryPath(self, file_desktop: str) -> FilePath:
        """Retorna uma instância de FilePath para o arquivo self.desktop_entry()"""
        return FilePath(self.desktop_entry(file_desktop))

    def show_dirs(self):
        _dirs = self.get_dirs()
        for _key in _dirs:
            print(f'{_key}'.ljust(19), end=' ')
            print(_dirs[_key])

    def create_dirs(self) -> bool:
        """
         Cria os diretórios de configuração.
        """
        if self.type_root:
            return False

        _dirs = self.config_dirs.getDirs()
        _appdirs = self.get_dirs()

        for KEY in _dirs:          
            mkdir(_dirs[KEY])

        for KEY in _appdirs:          
            mkdir(_appdirs[KEY])




def main():
    cfg: ConfDirs = ConfDirs()
    #cfg.showDirs()
    print(cfg.dirsJson())

    
if __name__ == '__main__':
    main()
