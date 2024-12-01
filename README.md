## 🏪 Sobre

Loja virtual desenvolvida durante a disciplina de Desenvolvimento Web Avançado.

Esse projeto faz parte da disciplina de Desenvolvimento Web Avançado, ministrada pelo professor Ricardo Maroquio. A disciplina faz parte do curso de Sistemas de Informação, ofertado pelo Instituto Federal do Espírito Santo - campus Cachoeiro de Itapemirim.

**Dupla:** [Gabriel Cardoso Girarde](https://github.com/GNobroga) e [Livia Guimarães de Jesus](https://github.com/4L1C3-R4BB1T).

---

## ⚙️ Como executar o projeto

❗ Para configurar e usar este projeto, siga as instruções no arquivo [projeto.md](https://github.com/4L1C3-R4BB1T/loja-virtual-dwa/blob/main/_docs/projeto.md).

Clone esse repositório:

```bash
https://github.com/4L1C3-R4BB1T/loja-virtual-dwa.git
```

Instale as dependências do projeto:

```bash
pip install -r .\requirements.txt
```

### 📟 Terminal 

Execute o comando abaixo para executar o projeto via terminal:

```bash 
uvicorn main:app --reload --port 8000
``` 

### 🐳 Docker 

Execute o comando abaixo para criar e executar o container docker:

```bash
docker compose up -d
```

Acesse o projeto pelo link:

```bash
http://localhost:8070
```

### 🐍 PythonDebug

No VSCode, execute com ```Ctrl + F5```. 

Acesse o projeto pelo link:

```bash
http://localhost:8000
```

### 🗎 Swagger

Acesse a documentação swagger pelo link:

```bash
http://localhost:8000/docs
```

---

## 👩‍💼Usuário Teste

```
email: joao@email.com
senha: 123aA@
```

---

## 🆕 Adição de Filtragem de Produtos por Categoria

![Busca de Produtos](https://github.com/4L1C3-R4BB1T/loja-virtual-dwa/blob/feature/categories/assets/1.png)
