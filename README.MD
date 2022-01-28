# Como rodar o projeto em minha máquina?

Considerando que você já fez o clone do projeto em sua máquina, siga os passos a seguir para rodar o projeto localmente em sua máquina.

1. Certifique-se de ter o <strong>virtualenv</strong> instalado, por mais que o mesmo seja opcional, é recomendado que utilize-o para evitar problemas futuros relacionados a versão, portanto, execute o seguinte comando em seu terminal:

```bash
pip3 install virtualenv
```

2. Após efetuar a instalação com sucesso, rode o seguinte comando para criar o seu ambiente virtual:

```bash
virtualenv venv
```

Caso um erro seja obtido, tente:

```bash
python3 -m virtualenv venv
```

3. Depois de ter feito a criação do <strong>Ambiente virtual</strong>, vamos ativar o mesmo, portanto, execute os comandos a seguir:

* Caso esteja utilizando <strong>Windows</strong>.

```bash
. .\venv\Scripts\activate
```

* Caso contrário

```bash
source venv/bin/activate
```

4. Com o ambiente criado e ativado, faremos a instação de todas as dependências do nosso projeto que podem ser encontradas no arquivo <strong>requirements.txt</strong>, para isso, temos o seguinte comando:

```bash
pip3 install -r requirements.txt
```

5. Por fim, temos finalmente tudo que é necessário para rodar o projeto, agora basta executar o arquivo <strong>setup.py</strong> que se encontra na raiz do projeto, para isso, execute:

```bash
python3 setup.py
```

# Como rodar os testes?

Um arquivo para executar todos os testes foi criado para facilitar esse processo, basta executar o mesmo com o seguinte comando:

```bash
python3 run_tests.py
```