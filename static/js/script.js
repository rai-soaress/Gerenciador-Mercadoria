function adicionarProduto() {
    const area = document.getElementById("area-produtos");
    const primeiraLinha = document.querySelector(".linha-produto");

    if (!area || !primeiraLinha) {
        return;
    }

    const novaLinha = primeiraLinha.cloneNode(true);

    novaLinha.querySelector("select").value = "";
    novaLinha.querySelector("input").value = "";

    area.appendChild(novaLinha);
}