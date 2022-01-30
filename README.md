# apps-conf

Lib para trabalhar com arquivos e diretórios, de configurações para aplicativos, em sistemas Linux e Windows.


# apps_conf.HOME:
   
   Diretório home do usuário.

# apps_conf.KERNEL_TYPE:

   Tipo de kernel do sistema (Windows, Linux, FreeBSD, ...)

# apps_conf.mkdir(path: str) -> bool:

   Cria um deretório.

# apps_conf.get_abspath(path: str) -> str:

   Retorna o caminho absoluto de um arquivo ou diretório.

# apps_conf.FilePath(path: str)

    Classe para trabalhar com arquivo, e obter algumas informações como:
    path()      - Caminho absoluto.
    exists()    - Verificar se o arquivo existe.
    name()      - Retorna o nome do arquivo, sem a extensão. 
    dirname()   - Retorna o diretório PAI do arquivo.
    basename()  - Retorna o nome do arquivo com a extensão.
    extension() - Retorna a extensão do arquivo, com base no nome.

# apps_conf.FileReader(file: FilePath)

    Classe para ler e gravar dados em um arquivo de texto.
    file = Objeto do tipo FilePath.

    