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