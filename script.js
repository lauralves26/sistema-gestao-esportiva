const API = "";

// Mostrar as telas
function mostrarTela(nome) {
    document.querySelectorAll(".tela").forEach(tela => {
        tela.hidden = tela.id !== nome;
    });

    if (nome === "modalidades") listarModalidades();
    if (nome === "treinadores") listarTreinadores();
    if (nome === "equipes") {
        carregarOpcoes();
        listarEquipes();
    }
}

// Comunicação com o Flask
async function requisicao(caminho, metodo = "GET", dados = null) {
    const opcoes = {
        method: metodo,
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (dados !== null) {
        opcoes.body = JSON.stringify(dados);
    }

    const resposta = await fetch(API + caminho, opcoes);
    const resultado = await resposta.json();

    if (!resposta.ok) {
        throw new Error(resultado.erro || "Erro na requisição");
    }

    return resultado;
}

// Mostrar mensagens
function mensagem(texto) {
    document.getElementById("mensagem").textContent = texto;
}

// Criar itens das listas com segurança
function preencherLista(idLista, registros, formatar) {
    const lista = document.getElementById(idLista);
    lista.replaceChildren();

    registros.forEach(registro => {
        const item = document.createElement("li");
        item.textContent = formatar(registro);
        lista.appendChild(item);
    });
}


document.getElementById("formModalidade")
    .addEventListener("submit", async function(evento) {

    evento.preventDefault();

    const dados = {
        nome: document.getElementById("nomeModalidade").value,
        descricao: document.getElementById("descricaoModalidade").value
    };

    try {
        await requisicao("/modalidades", "POST", dados);

        mensagem("Modalidade cadastrada com sucesso!");
        this.reset();
        listarModalidades();

    } catch (erro) {
        mensagem(erro.message);
    }
});


async function listarModalidades() {
    try {
        const dados = await requisicao("/modalidades");

        preencherLista(
            "listaModalidades",
            dados,
            modalidade => ${modalidade.nome} - ${modalidade.descricao || ""}
        );

    } catch (erro) {
        mensagem(erro.message);
    }
}


document.getElementById("formTreinador")
    .addEventListener("submit", async function(evento) {

    evento.preventDefault();

    const dados = {
        nome: document.getElementById("nomeTreinador").value,
        telefone: document.getElementById("telefoneTreinador").value
    };

    try {
        await requisicao("/treinadores", "POST", dados);

        mensagem("Treinador cadastrado com sucesso!");
        this.reset();
        listarTreinadores();

    } catch (erro) {
        mensagem(erro.message);
    }
});


async function listarTreinadores() {
    try {
        const dados = await requisicao("/treinadores");

        preencherLista(
            "listaTreinadores",
            dados,
            treinador => ${treinador.nome} - ${treinador.telefone || ""}
        );

    } catch (erro) {
        mensagem(erro.message);
    }
}


async function carregarOpcoes() {
    try {
        const modalidades = await requisicao("/modalidades");
        const treinadores = await requisicao("/treinadores");

        const campoModalidade =
            document.getElementById("modalidadeEquipe");

        const campoTreinador =
            document.getElementById("treinadorEquipe");

        campoModalidade.replaceChildren();
        campoTreinador.replaceChildren();

        modalidades.forEach(modalidade => {
            const opcao = new Option(
                modalidade.nome,
                modalidade.id_modalidade
            );

            campoModalidade.add(opcao);
        });

        treinadores.forEach(treinador => {
            const opcao = new Option(
                treinador.nome,
                treinador.id_treinador
            );

            campoTreinador.add(opcao);
        });

    } catch (erro) {
        mensagem(erro.message);
    }
}


document.getElementById("formEquipe")
    .addEventListener("submit", async function(evento) {

    evento.preventDefault();

    const dados = {
        nome: document.getElementById("nomeEquipe").value,
        categoria: document.getElementById("categoriaEquipe").value,
        id_modalidade: Number(
            document.getElementById("modalidadeEquipe").value
        ),
        id_treinador: Number(
            document.getElementById("treinadorEquipe").value
        )
    };

    try {
        await requisicao("/equipes", "POST", dados);

        mensagem("Equipe cadastrada com sucesso!");
        this.reset();
        listarEquipes();

    } catch (erro) {
        mensagem(erro.message);
    }
});


async function listarEquipes() {
    try {
        const dados = await requisicao("/equipes");

        preencherLista(
            "listaEquipes",
            dados,
            equipe => ${equipe.nome} - Categoria: ${equipe.categoria || "Não informada"}
        );

    } catch (erro) {
        mensagem(erro.message);
    }
}


mostrarTela("inicio");
