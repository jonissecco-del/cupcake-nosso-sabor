from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'faculdade_cupcake_key'

usuarios_cadastrados = {
    "999999999": "1234"
}

LISTA_CUPCAKES = [
    {"id": 1, "nome": "Brigadeiro Gourmet", "preco": 8.50, "imagem": "foto1.jpg", "desc": "Massa de chocolate belga com brigadeiro artesanal."},
    {"id": 2, "nome": "Red Velvet Real", "preco": 9.50, "imagem": "foto2.jpg", "desc": "Massa vermelha aveludada com cobertura de cream cheese."},
    {"id": 3, "nome": "Baunilha Multicolor", "preco": 7.50, "imagem": "foto3.jpg", "desc": "Clássica massa fofinha de baunilha coberta com confeitos."},
    {"id": 4, "nome": "Limão Merengue", "preco": 8.00, "imagem": "foto4.jpg", "desc": "Massa leve de limão com topo de merengue tostado."},
    {"id": 5, "nome": "Morango Especial", "preco": 9.00, "imagem": "foto5.jpg", "desc": "Massa de baunilha com pedaços frescos de morango."},
    {"id": 6, "nome": "Cenoura Premium", "preco": 8.00, "imagem": "foto6.jpg", "desc": "Massa tradicional de cenoura com calda de chocolate."},
    {"id": 7, "nome": "Caramelo Salgado", "preco": 9.00, "imagem": "foto7.jpg", "desc": "Massa de baunilha recheada com caramelo fluido."}
]

@app.route('/')
def home():
    return render_template('index.html', cupcakes=LISTA_CUPCAKES)

@app.route('/adicionar/<int:id_cupcake>', methods=['POST'])
def adicionar_carrinho(id_cupcake):
    if 'carrinho' not in session:
        session['carrinho'] = {}
    
    try:
        quantidade = int(request.form.get('quantidade', 1))
    except ValueError:
        quantidade = 1

    id_str = str(id_cupcake)
    
    for c in LISTA_CUPCAKES:
        if c['id'] == id_cupcake:
            if id_str in session['carrinho']:
                session['carrinho'][id_str]['quantidade'] += quantidade
            else:
                session['carrinho'][id_str] = {
                    "id": int(c["id"]),  # Garante que o ID salve como número inteiro
                    "nome": c["nome"],
                    "preco": c["preco"],
                    "imagem": c["imagem"],
                    "quantidade": quantidade
                }
            session.modified = True
            flash(f'{quantidade}x {c["nome"]} adicionado(s) ao carrinho!', 'sucesso')
            break
            
    return redirect(url_for('home'))

@app.route('/remover/<int:id_cupcake>')
def remover_carrinho(id_cupcake):
    if 'carrinho' in session:
        id_str = str(id_cupcake)
        if id_str in session['carrinho']:
            if session['carrinho'][id_str]['quantidade'] > 1:
                session['carrinho'][id_str]['quantidade'] -= 1
                flash(f'Uma unidade de {session["carrinho"][id_str]["nome"]} foi removida.', 'sucesso')
            else:
                nome_removido = session['carrinho'][id_str]['nome']
                session['carrinho'].pop(id_str)
                flash(f'{nome_removido} foi removido do seu carrinho.', 'sucesso')
                
            session.modified = True
            
    return redirect(url_for('ver_carrinho'))

@app.route('/carrinho')
def ver_carrinho():
    carrinho_dict = session.get('carrinho', {})
    itens_carrinho = list(carrinho_dict.values())
    
    total = sum(float(item['preco']) * int(item['quantidade']) for item in itens_carrinho)
    total_formatado = f"{total:.2f}".replace('.', ',')
    
    return render_template('carrinho.html', itens=itens_carrinho, total=total_formatado)

@app.route('/fechar_pedido')
def fechar_pedido():
    if not session.get('usuario'):
        flash("Você precisa estar logado para fechar o pedido! Por favor, faça login ou cadastre-se.", "erro")
        return redirect(url_for('login'))
        
    session.pop('carrinho', None)
    flash("Seu pedido foi enviado para nosso Whats 99999999. Logo entramos em contato!", "sucesso")
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        celular = request.form.get('celular')
        senha = request.form.get('senha')
        
        if celular in usuarios_cadastrados and usuarios_cadastrados[celular] == senha:
            session['usuario'] = celular
            flash('Login realizado com sucesso! Bem-vindo.', 'sucesso')
            return redirect(url_for('home'))
        else:
            flash('Celular ou senha incorretos. Tente novamente!', 'erro')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Você saiu da sua conta.', 'sucesso')
    return redirect(url_for('home'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        celular = request.form.get('celular')
        senha = request.form.get('senha')
        confirma_senha = request.form.get('confirma_senha')
        
        if not celular or not senha:
            flash('Por favor, preencha todos os campos.', 'erro')
        elif senha != confirma_senha:
            flash('As senhas não coincidem!', 'erro')
        elif celular in usuarios_cadastrados:
            flash('Este número de celular já está cadastrado!', 'erro')
        else:
            usuarios_cadastrados[celular] = senha
            flash('Cadastro realizado com sucesso! Faça seu login abaixo.', 'sucesso')
            return redirect(url_for('login'))
            
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)
