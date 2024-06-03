function formataCpf(e){
    var input = document.querySelector('#cpf')
    value = input.value
    if(isNaN(e.data)){
        input.value = value.substring(0, value.length-1)
        return
    }
    input.setAttribute("maxlength", "14");
    if(value.length == 3 || value.length == 7) input.value += "."
    if(value.length == 11) input.value += "-"
    limit = [3,7,11]
    if(limit.includes(value.length) && e.inputType == 'deleteContentBackward'){
        input.value = value.substring(0, value.length-1)  
    }
}

function formataTel(e){
    var input = document.querySelector('#telefone')
    value = input.value
    if(isNaN(e.data)){
        input.value = value.substring(0, value.length-1)
        return
    }
    input.setAttribute("maxlength", "14");
    if(value.length == 1) input.value = "(" + input.value
    if(value.length == 3) input.value += ")"
    if(value.length == 9) input.value += "-"
    limit = [1,3,9]
    if(limit.includes(value.length) && e.inputType == 'deleteContentBackward'){
        input.value = value.substring(0, value.length-1)
    }
}

function enviarForm(){
    var form = document.querySelector('#cadConsumidor')
    var nome = document.querySelector('#nome')
    var cpf = document.querySelector('#cpf')
    var email = document.querySelector('#email')
    var telefone = document.querySelector('#telefone')
    var senha = document.querySelector('#senha')
    var cSenha = document.querySelector('#cSenha')
    var pais = document.querySelector('#pais')
    var uf = document.querySelector('#uf')
    var cidade = document.querySelector('#cidade')

    if(!conferirNulo(nome.value, cpf.value, email.value, telefone.value, senha.value, cSenha.value, pais.value, uf.value, cidade.value)){
        return alert("Existe campos vazios")
    }
    if(!validarCpf(cpf.value)){
        return alert("CPF Inválido")
    }
    if(!validarSenha(senha.value, cSenha.value)){
        return alert("Senhas divergentes")
    } 
    return form.submit()
}

function validarCpf(e){
    return true
}

function validarSenha(senha, cSenha){
    if(senha == cSenha){
        return true
    }else{
        return false
    }
}

function conferirNulo(nome, cpf, email, telefone, senha, cSenha, pais, uf, cidade){
    /* console.log(nome, nome.length)
    console.log(cpf, cpf.length)
    console.log(email, email.length)
    console.log(telefone, telefone.length)
    console.log(senha, senha.length)
    console.log(cSenha, cSenha.length)
    console.log(pais, pais.length)
    console.log(uf, uf.length)
    console.log(cidade, cidade.length) */
    if(nome.length > 0 && cpf.length > 0 && email.length > 0 && telefone.length > 0 && senha.length > 0 && cSenha.length > 0 && pais.length > 0 && uf.length > 0 && cidade.length > 0){
        console.log("Verdadeiro")
        return true
    }
    console.log("Falso")
    return false
}

function checkBox(id){
    box = window.document.querySelector(id)
    if(box.checked == true){
        box.checked = false
    }else{
        box.checked = true
    }
}

function openFile(id){
    input = window.document.querySelector(id)
    if(input && document.createEvent) {
        var evt = document.createEvent("MouseEvents");
        evt.initEvent("click", true, false);
        input.dispatchEvent(evt);
    }
}

function showImg(event, id){
    var selectedFile = event.target.files[0]
    var banner = window.document.querySelector(id)
    var reader = new FileReader()
    reader.onload = function(event) {
    banner.style.background = `url(${event.target.result}) center/cover no-repeat`
    };

    reader.readAsDataURL(selectedFile);
}

function enviarForm2(){
    var form = window.document.querySelector('#cadPrimeiroAcesso')
    var imagem_loja =  window.document.querySelector('#imagem_loja').value
    var nome_fantasia = window.document.querySelector('#nome_fantasia').value
    var forma_pagamento = window.document.getElementsByName('forma_pagamento')
    var len = forma_pagamento.length;
    var list = []
    for (var i=0; i<len; i++){
        forma_pagamento[i].checked ? list.push(forma_pagamento[i].value):''
    }
    return form.submit()
}

passo=0
function tutorial(acao){
    div = document.querySelector('#tutorial')
    if(acao == 'avancar'){
        passo = passo + 1
    }
    if(acao == 'voltar'){
        if(passo == 1){
            return
        }
        passo = passo - 1
    }

    if(passo == 1){
        div.innerHTML = `
        <div class="modal" id="modal-tutorial">
        
        <h3>Bem-vindo ao Sr. Camelô!</h3>
        <p>Estamos animados para começar esta jornada juntos.</p>
        <p>Nosso mascote está pronto para apresentar o aplicativo.</p>
        <div class="img-modal">
            <img class="back" style="
                filter: brightness(0) saturate(100%) invert(92%) sepia(4%) saturate(0%) hue-rotate(186deg) brightness(97%) contrast(86%);
            " src="/static/images/back.svg">
            <img src="/static/images/mascote.png" alt="">
            <img class="advance" src="/static/images/advance.svg" onclick="tutorial('avancar')">
        </div>
        <p>Clique nas setas para prosseguir com o tutorial!</p>
        <p>Se você já conhece o nosso app, você também pode clicar no botão "Pular" abaixo.</p>
        </div>
        <button type="button" class="modal-btn" onclick="esconderTutorial()">Pular</button>`
    }else if (passo == 2) {
        div.innerHTML = `
        <div class="modal" id="modal-tutorial">
        
        <h3>Monte o perfil da sua loja!</h3>
        <p>Adicione uma imagem que represente seu negócio. </p>
        <p>Preencha com o nome da sua loja.</p>
        <div class="img-modal">
            <img class="back" style="filter: brightness(0) saturate(100%) invert(43%) sepia(85%) saturate(2798%) hue-rotate(3deg) brightness(105%) contrast(106%);" src="/static/images/back.svg" onclick="tutorial('voltar')">
            <img src="/static/images/tutorial2.png" alt="">
            <img class="advance" src="/static/images/advance.svg" onclick="tutorial('avancar')">
        </div>
        <p>Selecione as formas de pagamento que você aceitará.</p>
        </div>
        <button type="button" class="modal-btn" onclick="esconderTutorial()">Pular</button>`
    }else if(passo == 3){
        div.innerHTML = `
        <div class="modal" id="modal-tutorial">
        
        <h3>Cadastre seus produtos</h3>
        <p>Quando você clicar no botão 'Cadastrar Produtos', será direcionado para uma nova tela.</p>
        <p> Você poderá preencher o nome do produto, o preço, uma breve descrição e a categoria à qual o produto pertence.</p>
        <div class="img-modal">
            <img class="back" style="filter: brightness(0) saturate(100%) invert(43%) sepia(85%) saturate(2798%) hue-rotate(3deg) brightness(105%) contrast(106%);" src="/static/images/back.svg" onclick="tutorial('voltar')">
            <img src="/static/images/tutorial3.png" alt="">
            <img class="advance" style="filter: brightness(0) saturate(100%) invert(92%) sepia(4%) saturate(0%) hue-rotate(186deg) brightness(97%) contrast(86%);" src="/static/images/advance.svg">
        </div>
        <p>Para adicionar mais produtos, clique no botão redondo com o símbolo de '+'. Para excluir um produto, basta clicar no ícone da lixeira.</p>
        </div>
        <button type="button" class="modal-btn" onclick="esconderTutorial()">Finalizar</button>`
    }
}

function esconderTutorial(){
    div = document.querySelector('#tutorial')
    div.style.display='none'
}