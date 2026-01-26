'''
FP2526P2
autor: João Coelho
nº: 117964
'''

MINIMO_LETRAS_1_JOGADA = 2
MINIMO_LETRAS_JOGADA = 1
MAXIMO_LETRAS_JOGADA = 15
N_LETRAS_JOGADOR = 7
TAMANHO_TABULEIRO = 15
N_MIN_JOGADORES = 2
N_MAX_JOGADORES = 4
ALFABETO = {'A': 0, 'B': 1, 'C': 2, 'Ç': 3, 'D': 4, 'E': 5, 
            'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'L': 11, 
            'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 
            'S': 18, 'T': 19, 'U': 20, 'V': 21, 'X': 22, 'Z': 23}

#Minhas funções auxiliares 

def ordena_letras(alfabeto, conj):

    '''
    Ordena as letras de um conjunto numa lista

    Recebe o alfabeto considerado (dict)
    E um dicionário que representa o conjunto de letras (dict)
    Percorre o alfabeto e, ao encontrar uma dessas letras como chave do dicionário,
    acrescenta-a, valor vezes, à nova lista, garantindo ordenação correta
    Devolve a lista com os elementos do conjunto de letras ordenados

    dict, dict -> list
    '''

    letras_ordenadas = [] 
    for chave in alfabeto: 
        if chave in conj:  
            letras_ordenadas += [chave, ] * conj[chave]
    return letras_ordenadas


def ordena_palavras(lista_palavras): 
    
    '''
    Recebe uma lista de palavras(lista_palavras) e ordena-as por ordem lexicográfica

    list -> list
    '''

    return sorted(lista_palavras, key=lambda palavra: [ALFABETO[letra] for letra in palavra]) #funcao anonima


def gerador_linhas():
    
    '''
    Gera uma lista que corresponde a uma linha do tabuleiro
    Quando chamada, gera uma lista correspondente a uma linha do tabuleiro, 
    com 15 elementos (colunas) , em que cada elemento é o carater '.'
    Devolve essa lista
    {} -> list
    '''

    linha=[]
    for i in range (0,TAMANHO_TABULEIRO,1):
        linha += ['.', ]
    return linha


def vef_subpadrao(padrao_in, subpadrao, i, j): #i e j sao os iteraveis da funcao q a chama
    
    '''
    Recebe um padrão e verifica se o subpadrão é viável
    Recebe o padrão base (padrao_in), e um subpadrão obtido a partir dele,
    (subpadrao), também recebe os índices (i) e (j), que correspondem
    aos indíces da tabela de exemplo do enunciado, de modo a facilitar
    a sua implementação.
    Devolve True se for um subpadrão viável e False caso contrário
    '''

    passou_letra = False
    passou_espaco = False
    nao_letra_depois = False
    nao_letra_antes = False
    for elemento in subpadrao:
        if elemento in ALFABETO: #1
            passou_letra = True
        if elemento == '.': #2
            passou_espaco = True
        if passou_letra and passou_espaco:
            if i == 0:
                nao_letra_antes = True #3 a) #nunca tem letra antes
            else:
                if padrao_in[i-1] == '.': #3 a)
                    nao_letra_antes = True
            if j == len(padrao_in):
                nao_letra_depois = True #3 b) #nunca tem letra depois
            else:
                if padrao_in[j] == '.': #3 b) #não é j-1 por causa da natureza da tabela
                    nao_letra_depois=True
            if nao_letra_antes and nao_letra_depois:
                return True
            break
    return False


def calcula_pontos_palavra(palavra): #Por eficiência

    '''Recebe uma palavra e calcula os seus pontos, str-> int'''
    pontuacao = 0
    for letra in palavra:
        pontuacao += pontos[letra] #acede ao dict pontos
    return pontuacao


def gera_numero_aleatorio(estado):
    
    '''
    Recebe um inteiro positivo (estado)
    Devolve um número pseudo-aleatório através das operações xorshift
    int -> int
    '''
    estado ^= ( estado << 13) & 0xFFFFFFFF
    estado ^= ( estado >> 17) & 0xFFFFFFFF
    estado ^= ( estado << 5) & 0xFFFFFFFF
    return estado


def permuta_letras(letras, estado):
    
    '''
    Troca a ordem dos elementos da lista letras
    Recebe uma lista de letras e o estado inicial (inteiro positivo, para gerar número pseudo-aleatório
    Devolve uma lista permutada de acordo com o algoritmo de Fisher-Yates
    list, int -> list
    '''

    for i in range (len(letras) -1, 0, -1):
        estado = gera_numero_aleatorio(estado) #atualização do estado p/ a seguinte iteração
        j = estado % (i+1) #o módulo de (i+1) limita o numero gerado ao intervalo 0<=j<=i
        letras [j], letras[i] = letras[i], letras[j]


def elimina_str(palavra,padrao): 

    '''
    Elimina da palavra as letras já presentes no padrão do tabuleiro
    Recebe uma palavra (string) e um padrão (string)
    Copia-os para listas mutáveis
    Percorre a lista da palavra e se alguma letra já estiver na lista do padrão,
    percorre-a e elimina a primeira ocorrência dessa letra da lista do padrão,
    para as próximas iterações e da lista da palavra, como pretendido.
    Assim, Devolve a lista com as letras que o jogador usou
    
    str, str -> list
    '''
    
    palavra_lista=list(palavra) #converter em lista para poder eliminar ocorrencias
    padrao_lista=list(padrao)
    i=0
    while i < len(palavra_lista): #percorre a palavra
        j = 0
        if palavra_lista[i] in padrao_lista: 
            while j < len (padrao_lista):
                if padrao_lista[j] == palavra_lista[i]: #elimina p/ prox. iterações sem repetições
                    del(padrao_lista[j]) 
                    break                #Qnd elimina letra, avança p/ prox. iteração
                else:j+=1   
            del(palavra_lista[i]) #elimina a primeira ocorrencia da letra, na palavra
        else:
            i+=1
    return palavra_lista 


def ordena_letras_para_tuplo(palavra, alfabeto):
    
    '''
    Ordena letras de uma palavra num tuplo
    Pode receber uma palavra (string) ou uma lista com letras de uma palavra
    e o tuplo com as letras do abcedário considerado.
    Percorre as letras de letras, para ordenação e conta quantas vezes essa letra se repete
    Devolve o tuplo com as letras, no nº de vezes que se repetem, ordenadas.
    palavra, tuple -> tuple
    '''
    
    t = ()
    for letra in alfabeto: 
        occ = 0 #reinicia o contador para cada letra
        for letra_palavra in palavra: #para cada letra de letras, percorre as letras da palavra
            if letra_palavra == letra:  
                occ +=1 #Conta o nº de repetições de certa letra na palavra, occ=0 se não ocorrer
        t += (letra, ) * occ
    return t


def elimina_let_substitui_conj(pilha, jogador, palavra):
    
    '''
    Elimina do conjunto as letras jogadas, substituindo-as pelas últimas letras da pilha
    Recebe a pilha (list), o jogador (dict) e uma palavra (str) e recorre à função
    'elimina_let_conj' para eliminar as letras jogadas do conjunto do jogador e, para
    acrescentar novas letras ao conjunto, recorre à função 'distribui_letra' que as
    retirará da pilha.
    Devolve False se as letras a jogar não estiverem no conjunto e True caso contrário.
    list, jogador, str -> bool
    '''

    for letra in palavra:
        if letra not in jogador_letras(jogador):
            return False
    for letra in palavra: #outro ciclo p/ nao modificar em vao
        usa_letra(jogador, letra)
    distribui_letras(jogador, pilha, len(palavra))
    return True


def joga_palavra(tab, palavra, casa, direcao, conj_letras, vocab):
    
    '''
    Permite jogar uma palavra no tabuleiro
    Recebe o tabuleiro(tab), a palavra a inserir (string), a casa de partida (casa),
    a direcao (string), 'H' ou 'V', o conjunto de letras do jogador (conj_letras)
    e o vocabulário.
    Consoante as regras do jogo, a função tem um comportamento diferente se se trata
    da primeira jogada ou não. Recorre às funções 'testa_palavra_padrao', 'cria_casa',
    'insere_palavra', 'elimina_str', 'ordena_letras_para_tuplo', 'eh_tabuleiro_vazio', 
    'obtem_lin', 'obtem_col', 'incrementa_casa' e 'obtem_pontos'
    Devolve um tuplo vazio se a jogada não for válida, mas, se o for, devolve o tuplo
    com as letras jogadas pelo jogador
    tabuleiro, str, casa, str, conj_letras, vocab -> tuple
    '''

    res = ()
    #testar se a palavra cabe no tabuleiro
    if direcao == 'H':
        len_horz = TAMANHO_TABULEIRO - obtem_col(casa) + 1 #'H': Tamanho disponivel = total - posição inicial na linha (col) + 1
        if len(palavra) > len_horz:
            return res
    elif direcao == 'V':
        len_vert = TAMANHO_TABULEIRO - obtem_lin(casa) + 1 
        if len(palavra) > len_vert:
            return res
    
    casa_final = incrementa_casa(casa, direcao, len(palavra)-1)
    padrao_tabuleiro=obtem_padrao(tab, casa, casa_final)
    #o conjunto tem de conter todas as letras necessárias para formar a palavra
    if not testa_palavra_padrao(vocab, palavra, padrao_tabuleiro, conj_letras):
        return res
    
    #se for a primeira jogada
    if eh_tabuleiro_vazio(tab):
        if len(palavra) < MINIMO_LETRAS_1_JOGADA:
            return res
        meio = TAMANHO_TABULEIRO // 2 + 1  #TAMANHO_TABULEIRO sempre impar
        casa_central = cria_casa(meio,meio)
        cobre_casa_c = False
        for i in range (0, len(palavra), 1): #Ver se cobre a casa central
            casa_inc = incrementa_casa(casa, direcao, i)
            if casa_inc == casa_central:
                cobre_casa_c = True
                break
        if not cobre_casa_c:
            return res
    
    else: #já nao é primeira jogada:
        # a palavra tem de conter uma letra do padrao
        contem_peca_tab = False
        for letra in palavra:
            if letra in padrao_tabuleiro: #se houver uma letra da palavra no padrão, está na posiçao certa -> (testa_palavra_padrao)
                contem_peca_tab = True 
                break
        if not contem_peca_tab: 
            return res
        # o jogador deve utilizar pelo menos uma letra do seu conjunto, tem de preencher pelo menos uma casa
        if '.' not in padrao_tabuleiro: 
            return res
        
        #palavra tem de estar no vocab
        if obtem_pontos(vocab, palavra) == 0: 
            return res
    
    # Se a jogada é válida
    insere_palavra(tab, casa, direcao, palavra)
    #Tem de se retirar as letras que já estão no padrão, pois não fazem parte do conjunto
    palavra_final = elimina_str(palavra, padrao_tabuleiro)
    res += ordena_letras_para_tuplo(palavra_final, ALFABETO)
    return res

################################TAD CASA#####################################

'''
O TAD imutável casa é usado para representar uma casa do tabuleiro de Scrabble
Representação interna: tuplo
'''

def cria_casa(lin,col):
    
    '''
    Recebe uma abcissa (lin) e ordenada (col) e devolve a casa correspondente
    Recebe dois inteiros positivos l (linha),c (coluna),
    Valores entre 1 e o tamanho do tabuleiro
    Verifica os seus argumentos
    Devolve um tuplo correspondente à casa do tabuleiro (linha, coluna)
    int, int -> casa
    '''

    if type (lin) != int or type (col) != int or lin> TAMANHO_TABULEIRO or lin<1 or col> TAMANHO_TABULEIRO or col<1:
        raise ValueError('cria_casa: argumentos inválidos')
    return (lin,col)


def obtem_col(c):

    '''Devolve a coluna (col) da casa (c), casa -> int'''

    return c[1]


def obtem_lin(c):

    '''Devolve a linha (lin) da casa (c), casa -> int'''

    return c[0]


def eh_casa(arg):
    
    '''
    Indica se um argumento é um TAD casa
    
    Faz a verificação do argumento, se tal se confirmar,
    Devolve True, e False caso contrário
    universal ->bool
    '''

    if type (arg) == tuple and len(arg)==2:
        if type (obtem_lin(arg)) == int and type(obtem_col(arg)) == int:
            if obtem_lin(arg)<= TAMANHO_TABULEIRO and obtem_lin(arg)>=1:
                if obtem_col(arg)<= TAMANHO_TABULEIRO and obtem_col(arg)>=1:
                    return True
    return False


def casas_iguais (c1,c2):
    
    '''
    Indica se (c1) e (c2) são casas e são iguais
    Devolve True, caso se verifique e False caso contrário
    universal, universal -> bool
    '''

    if eh_casa(c1) and eh_casa(c2):
        if c1 == c2:
            return True
    return False


def casa_para_str(c):

    '''Devolve a cadeia de caracteres que representa uma casa, casa -> str '''
    
    return f'({obtem_lin(c)},{obtem_col(c)})'


def str_para_casa(s):

    '''Devolve a casa representada pela cadeia de caracteres (s), str -> casa'''

    s_limpa = s.strip().strip('()') #remove espaços, parentesis e plicas
    c=s_limpa.split(',') #transforma em lista com os elemntos
    linha = int(c[0].strip())
    coluna= int(c[1].strip())
    return cria_casa(linha,coluna)

#################################TAD JOGADOR#################################

'''
O TAD jogador é usado para representar um jogador do jogo Scrabble,
a sua pontuação e letras. Os jogadores podem ser humanos ou agentes.
Representação interna: dicionário
'''

#Operações básicas auxiliares do TAD jogador

def cria_duplicado_jog(jog):
    
    '''
    Recebe um jogador (jog) e devolve a sua cópia
    jog -> jog_duplicado
    '''

    duplicado = cria_humano('duplicado')
    duplicado['id'] = jog['id']
    duplicado['pontos'] = jog['pontos']
    duplicado['letras'] = jog['letras'].copy()
    return duplicado


def jogador_humano(j): #devolve true se humano, false caso contrário

    '''Devolve True se o jogador é humano e False se é agente, jogador -> bool'''
    
    return j['humano']


def numero_letras(j):

    '''Devolve o numero de letras conjunto do jogador (j), jogador -> int'''
    
    return len(jogador_letras(j))

#Operações básicas do TAD jogador

def cria_humano(nome):

    '''
    Cria um jogador humano.
    Recebe uma cadeia de carcateres não vazia a representar o nome do jogador
    Verifica se o argumento é válido, gerando um erro se não o for
    Devolve o jogador de Scrabble humano com 0 pontos e sem letras
    
    str -> jogador
    '''

    if type (nome) != str or nome == "": #o nome pode ser 'DIFICIL' por ex!
        raise ValueError('cria_humano: argumento inválido')
    return {'humano': True, 'id': nome, 'pontos': 0, 'letras': {}}


def cria_agente (nivel):

    '''
    Recebe uma cadeia de carcateres a representar o nível do jogador,
    ('FACIL', 'MEDIO' ou 'DIFICIL')
    Verifica se o argumento é válido, gerando um erro se não o for.
    Devolve o jogador de Scrabble humano com 0 pontos e sem letras
    '''

    if type(nivel) != str or nivel not in ('FACIL', 'MEDIO', 'DIFICIL'):
        raise ValueError('cria_agente: argumento inválido')
    return {'humano': False, 'id': nivel, 'pontos': 0, 'letras': {}}


def jogador_identidade(j):
    
    '''
    Devolve o nome do jogador j se é um jogador humano
    ou o nível se é um jogador agente.
    jog -> str
    '''

    if j['humano']:
        return j['id']
    else:
        return j['id']
    

def jogador_pontos(j): 

    '''Devolve os pontos do jogador j, jogador->int'''
    
    return j['pontos']


def jogador_letras(j):

    '''
    Devolve a cadeia de carateres ordenada com todas as letras do jogador (j)
    jogador -> str
    '''

    conj_letras = j['letras']
    letras_ordenadas = ordena_letras(ALFABETO, conj_letras)
    return "".join(letras_ordenadas)


def recebe_letra(j, l): 
    
    '''
    Modifica destrutivamente o jogador (j) acrescentado a letra (l) às suas letras
    Devolve o próprio jogador
    jogador, str -> jogador
    '''

    if l in j['letras']:
        j['letras'][l] += 1 #adiciona um valor à chave
    else:
        j['letras'].update({l: 1}) #se não pertencer, adiciona o par letra:valor
    return j


def usa_letra(j,l):
    
    '''
    Modifica modifica destrutivamente o jogador (j) retirando a letra (l) às suas letras
    Devolve o próprio jogador
    jogador, str -> jogador
    '''

    if l in j['letras']:
        j['letras'][l] -= 1
    else:
        pass #prov nao fazer nada
    return j


def soma_pontos (j, p):
    
    '''
    Modifica destrutivamente o jogador (j) somando os pontos (p) à sua pontuação atual
    Devolve o próprio jogador
    jogador, int -> jogador
    '''

    j['pontos'] += p
    return j


def eh_jogador(arg):
    
    '''
    Recebe um argumento (arg)
    Devolve True caso seja um TAD jogador e False caso contrário
    universal -> bool
    '''

    if type(arg) != dict or len(arg) != 4:
        return False
    
    try:
        humano = jogador_humano(arg)
        id = jogador_identidade(arg)
        pontos = jogador_pontos(arg)
        conj_letras = jogador_letras(arg)

        if type(id) != str or type (humano) != bool:
            return False
        if type(pontos) != int or pontos < 0 or len(str(pontos)) > 3:
            return False
        if type (conj_letras) != str:
            return False
        n_letras = numero_letras(arg)
        if n_letras>7:
            return False
        for letra in conj_letras:
            if letra not in ALFABETO:
                return False
        return True
    except (TypeError, KeyError): #testes privados
        return False


def eh_humano(arg):
    
    '''
    Recebe um argumento (arg)
    Verifica se é um TAD jogador e se é humano
    Devolve True se a condição se verificar e False caso contrário
    universal -> bool
    '''

    return eh_jogador(arg) and jogador_humano(arg)


def eh_agente(arg):
    
    '''
    Recebe um argumento (arg)
    Verifica se é um TAD jogador e se é um agente
    Devolve True se a condição se verificar e False caso contrário
    universal -> bool
    '''

    return eh_jogador(arg) and (not jogador_humano(arg))


def jogadores_iguais(j1, j2):

    '''
    Recebe dois argumentos (j1) e (j2)
    Verifica se ambos são TAD jogador e se são iguais
    Devolve True se a condição se verificar e False caso contrário
    universal, universal -> bool
    '''

    if not (eh_jogador(j1) and eh_jogador(j2)):
        return False
    
    #comparar componentes um a um (TAD)
    if jogador_identidade(j1) != jogador_identidade(j2):
        return False
    if jogador_humano(j1) != jogador_humano(j2):
        return False
    if jogador_pontos(j1) != jogador_pontos(j2):
        return False
    if jogador_letras(j1) != jogador_letras(j2):
        return False
    return True


def jogador_para_str(t):
    
    '''
    Recebe um jogador (t) 
    Recorre à função 'ordena_letras' para as ordenar
    Devolve a string que o representa
    jogador -> str
    '''

    id = jogador_identidade(t)
    pontos = jogador_pontos(t)
    str_letras=jogador_letras(t)
    if jogador_humano(t):
        if str_letras: #Para os testes publicos:
            res = f"{id} ({pontos:>3}): {' '.join(str_letras)}"
        else:
            res = f"{id} ({pontos:>3}):" #se nao houver letras, nao imprime um espaço a mais a seguir a ':'
    else:
        if str_letras:
            res = f"BOT({id}) ({pontos:>3}): {' '.join(str_letras)}"
        else:
            res = f"BOT({id}) ({pontos:>3}):"
    return res

#####################TAD VOCABULARIO#######################

'''
O TAD vocabulario é usado para representar o conjunto de palavras
que podem ser utilizadas durante o jogo.
Adicionalmente, o TAD vocabulario regista a pontuação das
palavras utilizando a pontuação das letras abaixo representada em pontos.
Representação interna: dicionário
O dicionário que representa o vocabulário está organizado por tamanho de palavra,
primeira letra e ordem lexicográfica
ex: {3: {'A': ['AÇO', 'ALI'], 'B': ['BIA']}, 5: {'A': ['AMIGO']}, 9: {'A': ['AUTOCARRO']}}
'''

pontos = {
        'A': 1, 'B': 3, 'C': 2, 'Ç': 3, 'D': 2, 'E': 1,
        'F': 4, 'G': 4, 'H': 4, 'I': 1, 'J': 5, 'L': 2,
        'M': 1, 'N': 3, 'O': 1, 'P': 2, 'Q': 6, 'R': 1,
        'S': 1, 'T': 1, 'U': 1, 'V': 4, 'X': 8, 'Z': 8 }

#Operações básicas do TAD vocabulario

def vocab_ord_pontos_igual_len_let(vocabulario, comp, letra): 
    
    '''
    Devolve um vocabulário ordenado por pontuação e ordem lexicográfica
    Recebe o TAD vocabulario (vocabulario), o comprimento das palavras
    a considerar (comp) e a primeira letra dessas palavras (letra)
    Constrói o dicionário ordenado por ordem decrescente de pontos
    com uma sublista de palavras ordenadas, de compriemnto (comp) 
    e primeira letra (letra), para cada valor de pontuação.
    Devolve esse dicionário
    vocabulario, int, str -> dict
    ex:  #{17: ['AXZ'], 5: ['AÇO'], 4: ['ADO', 'ALO']} 
    '''

    res = {}
    if comp in vocabulario and letra in vocabulario[comp]: #vef. extra p/ não gerar erros
        for elemento in vocabulario[comp][letra]:
            pontuacao = calcula_pontos_palavra(elemento) #correcao, nao usa obtem_pontos por eficiencia
            if pontuacao in res:
                res[pontuacao].append(elemento)
            else:
                res.update({pontuacao: [elemento, ]})
    return dict(sorted(res.items(), reverse=True)) #ordena ordem decres


def obtem_palavra_par(par):

    '''Devolve a palavra do tuplo par (palavra, pontos), tuple -> str'''

    return par[0]


def obtem_pontos_par(par):
    
    '''Devolve os pontos do tuplo par (palavra, pontos), tuple -> str'''

    return par[1]

#Operações básicas do TAD vocabulario

def cria_vocabulario(v):

    '''
    Recebe um tuplo (v) com palavras e devolve o vocabulário obtido a partir dele
    Verifica a validade do seu argumento, gerando um erro caso não se verifique
    Devolve o vocabulário na representação considerada para este TAD
    Faz uso da função ordena_palavras para as ordenar
    tuple -> vocabulario
    '''

    if type (v) != tuple or len(v) < 1:
        raise ValueError('cria_vocabulario: argumento inválido')
    for palavra in v:
        if type (palavra) != str:
            raise ValueError('cria_vocabulario: argumento inválido')
        if len(palavra) < MINIMO_LETRAS_1_JOGADA or len(palavra) > MAXIMO_LETRAS_JOGADA:
            raise ValueError('cria_vocabulario: argumento inválido')
        for letra in palavra:
            if letra not in ALFABETO:
                raise ValueError('cria_vocabulario: argumento inválido')
            
    #ordenar palavras por comprimento e por primeira letra
    vocabulario = {}
    for i in range (MINIMO_LETRAS_1_JOGADA, MAXIMO_LETRAS_JOGADA+1, 1): #criar as chaves por tamanho
        for palavra in v:
            if len(palavra) == i:
                if i not in vocabulario:
                    vocabulario.update({i: {}})
                if palavra[0] in vocabulario[i]: #criar as sub_chaves por primeira letra
                    vocabulario[i][palavra[0]].append(palavra)
                else:
                    vocabulario[i].update({palavra[0]: [palavra, ]})

    #ordem lexicográfica nas sub_listas
    for i in vocabulario:
        for letra in vocabulario[i]:
            vocabulario[i][letra] = ordena_palavras(vocabulario[i][letra])
    return vocabulario


def obtem_pontos(vocabulario, palavra):

    '''devolve os pontos da palavra do vocabulário
    ou 0 caso não se encontre, vocabulario, str -> int'''

    pontuacao = 0
    comp = len(palavra)
    letra = palavra[0]
    if comp in vocabulario and letra in vocabulario[comp]: #vef. extra
        if palavra in vocabulario [comp][letra]:
            pontuacao = calcula_pontos_palavra(palavra)
    return pontuacao


def obtem_palavras(vocabulario, comp, letra): 

    '''
    Obtem as palavras e pontuação do vocabulário com o comprimento e 1ª letra pretendidos
    Devolve um tuplo de pares que correspondem a todas as palavras
    de comprimento (comp) e de primeira lera (letra), cada par do tuplo
    contém a palavra e a respetiva pontuação.
    É considerada a ordem dada pela função 'vocab_ord_pontos_igual_len_let'
    vocabulario, int, str -> tuple
    '''

    res = ()
    sub_dict_ordenado= vocab_ord_pontos_igual_len_let(vocabulario, comp, letra) 
    for pontos in sub_dict_ordenado:
        for elemento in sub_dict_ordenado[pontos]:
            res += ((elemento, pontos), )
    return res


def testa_palavra_padrao (vocabulario, palavra, padrao, letras):
    
    '''
    Verifica se um padrão pode ser preenchido por uma palavra
    Recebe o vocabulario, uma palavra (string), um padrão (string), formado pelo caracter '.' 
    e por letras, e um conjunto de letras (str).
   
    Verifica se é possível formar essa palavra preenchendo nos espaços do padrao 
    com o carater '.', as letras no conjunto de letras.
    Prossegue a verificação, caracater a caracter, dado que as letras verificadas 
    não podem ser verificadas novamente
    Devolve True se for possível fazê-lo
    Devolce False, caso contrário.
    
    vocabulario, string, string, string -> bool
    '''
    
    chave_1 = len(palavra)
    chave_2 = palavra[0]
    contido = False
    if chave_1 in vocabulario and chave_2 in vocabulario[chave_1]:
        if palavra in vocabulario[chave_1][chave_2]:
            contido = True
    if not contido:
        return False
    
    elif len (padrao) != len (palavra):
        return False
    letras_disp= list(letras)
    for i in range (len(padrao)):
        if padrao [i] != palavra [i] and padrao [i] != '.': #se a letra no padrao nao constar na mesma pos. na palavra
            return False
        elif padrao [i] == '.': #ver se as letras que temos sao suficientes para preencher o padrao
            letra = palavra[i]
            if letra not in letras_disp: #se a letra a preencher ja nao estiver disp
                return False
            else:
                letras_disp.remove(letra)
    return True


def ficheiro_para_vocabulario(nome_fich):
    
    '''
    Cria um vocabulário baseado nas palavras do ficheiro com o nome 'nome_fich'
    Recebe o nome do ficheiro (nome_fich), lê-o e, se a palavra cumprir os requisitos,
    adiciona a um tuplo com as palavras que criarão o vocabulario
    Devolve o vocabulário baseado desse tuplo
    str -> vocabulario
    '''

    with open (nome_fich, 'r') as file:
        palavras=file.readlines()
    palavras_sem_rep = set() #para questões de eficência, e p/ passar testes.
    for palavra in palavras:
        passou = True
        palavra = palavra.strip(' ').strip('\n').upper()
        if len(palavra) < MINIMO_LETRAS_1_JOGADA or len(palavra) > MAXIMO_LETRAS_JOGADA:
            passou = False
        if palavra == '':
            passou = False
        if passou:
            for letra in palavra:
                if letra not in ALFABETO:
                    passou = False
                    break
        if passou:
            palavras_sem_rep.add(palavra) #O set já ignora duplicados

    return cria_vocabulario(tuple(palavras_sem_rep))


def vocabulario_para_str(vocabulario): 
    
    '''
    Devolve a string que representa o vocabulário
    Recebe o vocabulário (vocabulario) e concatena todas as suas palavras numa string,
    separadas pelo caracter de mudança de linha.
    vocabulario -> str
    '''

    res = ""
    for tamanho in sorted(vocabulario.keys()):
        for letra_in in sorted(vocabulario[tamanho].keys()): #para ordenar os subdicts de chaves de primeira letra
            if len (vocabulario[tamanho][letra_in]) > 1: #se houver mais q uma palavra com a mesma letra e mesmos pontos
                #ordenar de acordo com ordem de obtem_palavras
                tuplo_ordenado = obtem_palavras(vocabulario, tamanho, letra_in)
                for sub_tuplo in tuplo_ordenado:
                    res += f"{sub_tuplo[0]}\n"
            else:
                res += f"{vocabulario[tamanho][letra_in][0]}\n"
    return res.rstrip('\n') #remove \n do fim

####################################TAD TABULEIRO#######################################

'''
O TAD tabuleiro é usado para representar um tabuleiro do jogo Scrabble 
e as letras nele colocadas.
Representação interna: lista
'''

#Operações básicas do TAD tabuleiro

def cria_tabuleiro(): 

    '''
    Devolve um tabuleiro de Scrabble vazio
    Quando invocada, gera um tabuleiro, que corresponde a uma 
    lista com TAMANHO_TABULEIRO listas,
    (cada uma corresponde a uma linha), geradas pela função 'gerador_linhas'
    Devolve o tabuleiro
    {} -> tabuleiro
    '''

    tab=[]
    for i in range (0,TAMANHO_TABULEIRO,1):
        tab += [gerador_linhas(), ]
    return tab


def obtem_letra(t, c):

    '''devolve a letra contida na casa (c) do tabuleiro (t), tabuleiro, casa -> str'''

    valor = t [obtem_lin(c)-1] [obtem_col(c)-1]
    return valor


def insere_letra(t,c,l): 

    '''Modifica destrutivamente o tabuleiro inserindo a letra (l) na casa (c) 
    do tabuleiro (t).Devolve o tabuleiro, tabuleiro, casa, str -> tabuleiro'''

    t[obtem_lin(c)-1] [obtem_col(c)-1] = l
    return t


def eh_tabuleiro(arg):

    '''
    Recebe um argumento (arg) e devolve True se arg é um tabuleiro e False caso contrário
    universal -> bool
    '''

    if not (type (arg) == list and len(arg) == TAMANHO_TABULEIRO):
        return False
    for linha in arg:
        if type (linha) != list or len (linha)!= TAMANHO_TABULEIRO:
            return False
        for elemento in linha:
            if elemento not in ALFABETO:
                if elemento != '.':
                    return False
    return True


def eh_tabuleiro_vazio(arg):
    
    '''
    Recebe um argumento (arg) e devolve True se arg é um tabuleiro e é vazio e False caso contrário
    '''

    if not (type (arg) == list and len(arg) == TAMANHO_TABULEIRO):
        return False
    for linha in arg:
        if type (linha) != list or len (linha)!= TAMANHO_TABULEIRO:
            return False
        for elemento in linha:
            if elemento != '.':
                return False
    return True


def tabuleiros_iguais(t1,t2):
    
    '''
    Indica se (t1) e (t2) são tabuleiros e se são iguais
    Devolve True, caso se verifique e False caso contrário
    universal, universal -> bool
    '''

    if eh_tabuleiro(t1) and eh_tabuleiro(t2):
        if t1 == t2:
            return True
    return False


def tabuleiro_para_str(t):
    
    '''
    Constrói a representação visual do tabuleiro
    Recebe um tabuleiro (t)
    Cria uma string que é concatenada sucessivamente até ser obtido o tabuleiro
    Devolve a cadeia de caracteres que o representa
    tabuleiro -> str
    '''

    tab_str = '                       1 1 1 1 1 1\n'
    tab_str += '     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5\n'
    tab_str += '   +-------------------------------+\n'
    for linha in range (0, len(t), 1):
        tab_str += f'{linha+1:>2} |' #linha 0 da lista -> linha 1 do tabuleiro
        for coluna in range(0,len(t),1):
            tab_str += f' {t[linha][coluna]}' #procura o elemento na posicao [linha][coluna]
        tab_str += " |\n"
    tab_str += '   +-------------------------------+'
    return tab_str

#---------------------------------------------------------------------------------------------#
##################################FUNÇÕES DE ALTO NÍVEL########################################
#---------------------------------------------------------------------------------------------#

def incrementa_casa (c, d, s):
    
    '''
    Incrementa a casa c, na direção d, a distância s
    Recebe uma casa(c), uma direção ('H' ou 'V') e uma distância (s), inteiro positivo.
    Devolve a casa de um tabuleiro de Scrabble a seguir de c, na direção d
    e a distância s. Caso não exista, devolve a casa c
    casa, str, int -> casa
    '''

    linha = obtem_lin(c)
    coluna = obtem_col(c)
    if d == 'H':
        if coluna + s > TAMANHO_TABULEIRO:
            return c
        return cria_casa(linha, coluna+s)
    elif d == 'V':
        if linha + s > TAMANHO_TABULEIRO:
            return c
        return cria_casa(linha+s, coluna)
    

def distribui_letras (jog, saco, num):
    
    '''
    Retira um máximo de num letras do final da lista saco, 
    acrescentando-as ao jogador jog
    Recebe o jogador(jog), uma lista de letras (saco) e o
    número máximo de letras a retirar da lista e a colocar
    no jogador
    Modifica destrutivamente a lista e o jogador
    Devolve o próprio jogador
    jogador, list, int -> jogador
    '''

    if saco == []:
        return jog
    else:
        maximo = num
        if len(saco) < num:
            maximo = len(saco)
        for i in range (maximo):
            ultima_letra = saco.pop() #apaga o ultimo elemento da lista
            recebe_letra(jog, ultima_letra)
        return jog
    

def procura_palavra_padrao(vocabulario, padrao, letras, min_pontos):
    
    '''
    Procura a palavra com maior pontuação num certo padrão
    Recebe o vocabulário(vocabulário), a cadeia de caracteres que representa
    o padrão (padrao), uma cadeia de caracteres que representa as letras
    do jogador (letras) e um inteiro positivo que representa o mínimo de pontos
    da palavra a procurar (min_pontos)
    Recorre à função 'obtem_palavras' para as obter e à função 'testa_palavra_padrao'
    para  garantir que sa palavra procurada é jogável no padrão
    Devolve a palavra obtida com mais pontuação, com o mínimo de pontos pretendido
    e, no caso de existirem várias palavras com essa pontuação é devolvida a primeira 
    em ordem lexicográfica.
    Caso a função não encontre nenhuma palavra, devolve o tuplo ('', 0)    
    
    vocabulario, str, str, int -> tuple
    '''

    if padrao[0] != '.': #Se começar com letra
        palavras_possiveis=obtem_palavras(vocabulario, len(padrao), padrao[0]) #ja vem ordenado por pontos
        for par in palavras_possiveis:
            if testa_palavra_padrao(vocabulario, obtem_palavra_par(par), padrao, letras): 
                if obtem_pontos_par(par) >= min_pontos: 
                    return par
        return ('', 0)
    
    else: #se começar por '.', tem de se testar para todas as letras do jogador
        pares_possiveis = ()
        letras_ordenadas = ordena_palavras(list(letras))
        for letra in letras_ordenadas:
            palavras_possiveis=obtem_palavras(vocabulario, len(padrao), letra)
            for par in palavras_possiveis:
                if testa_palavra_padrao(vocabulario, obtem_palavra_par(par), padrao, letras): 
                    if obtem_pontos_par(par) >= min_pontos:    
                        pares_possiveis += (par, )
        if not pares_possiveis:
            return ('',0)
        melhor_par = pares_possiveis[0]
        #Atualização por variável de estado do melhor par
        for par in pares_possiveis:
            palavra_atual = obtem_palavra_par(par)
            pontos_atual = obtem_pontos_par(par)
            tem_mais_pontos = pontos_atual > obtem_pontos_par(melhor_par)
            tem_pontos_iguais = pontos_atual == obtem_pontos_par(melhor_par)
            #É relevante porque se pontos iguais, vem a primeira em ordem lexicográfica.
            melhor_palavra = obtem_palavra_par(melhor_par)
            lista_2_palavras = [palavra_atual, melhor_palavra]
            lista_2_palavras_ordenadas = ordena_palavras(lista_2_palavras)
            palavra_antes = lista_2_palavras_ordenadas[0]
            if tem_mais_pontos or (tem_pontos_iguais and palavra_antes==palavra_atual):
                melhor_par = par
        
        return melhor_par
    

def obtem_padrao(t, i, f):

    '''
    Obtem o padrão entre a casa inicial (i) e a casa final (t) do tabuleiro (t)
    Recebe o tabuleiro (t), a casa inicial (i) e a casa final (f)
    Procura no tabuleiro, através da função 'incrementa_casa' e 'obtem_letra'
    as letras de cada casa do padrão e concatena-as, devolvendo a cadeia
    de carcateres resultante
    
    tabuleiro, casa, casa -> str
    '''

    padrao = ""
    if obtem_lin(i) == obtem_lin(f): #se linhas iguais, direcao H
        tamanho = obtem_col(f) - obtem_col(i) + 1
        for j in range (0, tamanho, 1):
            casa_h = incrementa_casa(i, 'H', j)
            padrao += obtem_letra(t, casa_h) #faz a concatenação das letras até atingir o tamanho inserido
    elif obtem_col(i) == obtem_col(f): #se colunas iguais, direcao V
        tamanho = obtem_lin(f) - obtem_lin(i) + 1
        for j in range (0, tamanho, 1):
            casa_v = incrementa_casa(i, 'V', j)
            padrao += obtem_letra (t, casa_v)
    return padrao


def insere_palavra (t, c, d, p):
    
    '''
    Insere, no tabuleiro, uma palavra, a partir casa e na direção escolhidas
    Recebe o tabuleiro (t), uma casa (c), a string direção (d) 
    ('H' - Horizontal; 'V' - Vertical) e a palavra a inserir no tabuleiro (string)
    Recorre à função 'incrementa_casa' e 'insere_letra' para aceder e modificar o tabuleiro
    Devolve o tabuleiro com a palavra que parte da casa escolhida ,
    para a direita (direção = 'H), ou para baixo (direção = 'V')
    tabuleiro, casa, str, str -> tabuleiro
    '''

    for s in range (0, len(p), 1):
        casa_a_inserir = incrementa_casa(c, d, s)
        t = insere_letra (t, casa_a_inserir, p[s])
    return t


def obtem_subpadroes(t, i, f, l):
    
    '''
    Obtem todos os subpadrões viáveis ordenados a partir do padrão principal
    Recebe o tabuleiro(t), a casa inicial (i), a casa final (f), e um inteiro 
    positivo (l) que indica o máximo de espaços livres do subpadrão a procurar
    Recorre à função 'vef_subpadrao' para saber se é um subpadrão viável
    Devolve dois tuplos, um que contém todos os subpadrões viáveis e outro
    que contém a casa inicial de cada um desses subpadrões, respetivamente
    tabuleiro, casa, casa, int -> tuple
    '''

    l1=[]
    l2=[]
    if obtem_lin(i) == obtem_lin(f):
        direcao = 'H'
    else:
        direcao = 'V'
    
    padrao_in = obtem_padrao(t, i, f)
    #Obter os subpadrões por fatiamento
    for k in range (0, len(padrao_in), 1):
        padrao_k = padrao_in[k:] #reduzir o padrão à esquerda
        for m in range (len(padrao_in), 0, -1): 
            padrao_m = padrao_k[:m-k] #Reduzir o padrão à direita de acordo com a tabela
            if k < m: #a linha diagonal da tabela so aceita valores acima dela
                if vef_subpadrao(padrao_in, padrao_m, k, m):
                    l1.append(padrao_m)
                    casa=incrementa_casa(i, direcao, k) #descobrir a casa inicial do subpadrão
                    l2.append(casa)
    
        #verif. máx l espaços livres
        i_padrao = 0
        while i_padrao < len(l1): #percorrer a lista de subpadrões
            conta_l=0
            for elemento in l1[i_padrao]: #conta o numero de espaços livres
                if elemento == '.':
                    conta_l +=1
            if conta_l > l: #se os espaços livres forem maiores que l, elimina o subpadrão
                l1.pop(i_padrao)
                l2.pop (i_padrao)
            else:
                i_padrao+=1 #se passar o 'teste', avança uma iteração
            
    return tuple(l1), tuple(l2)


def gera_todos_padroes(t, l):
    
    '''
    Gera todos os padrões de um tabuleiro (t) com o máximo de (l) espaços livres
    Recebe o tabuleiro(t) e um inteiro positivo (l)
    Gera primeiro todos os subpadrões de cada linha do tabuleiro e depois
    os subpadrões de cada coluna do tabuleiro
    Recorre à função obtem_subpadroes para obter todos os subpadrões de cada
    linha/coluna do tabuleiro
    Devolve um tuplo com todos os subpadrões viáveis, outro com as casas iniciais
    e outro com a direção ('H' ou 'V') de cada subpadrão, respetivamente
    '''
    t1 = ()
    t2 = ()
    t3 = ()
    #primeiro os subpadroes de cada linha do tabuleiro (H)
    for i_linha in range(TAMANHO_TABULEIRO):
        casa_i = cria_casa(i_linha +1, 1) #i = 0 -> linha = 1
        casa_f= cria_casa(i_linha+1, TAMANHO_TABULEIRO)
        p_poss, casas = obtem_subpadroes(t, casa_i, casa_f, l)
        t1 += p_poss
        t2 += casas
        t3 += ('H', ) * len(p_poss)
    #depois os subpadroes de cada coluna do tabuleiro (V)
    for i_coluna in range (TAMANHO_TABULEIRO):
        casa_i = cria_casa(1, i_coluna+1)
        casa_f = cria_casa(TAMANHO_TABULEIRO, i_coluna+1)
        p_poss, casas = obtem_subpadroes(t, casa_i, casa_f, l)
        t1 += p_poss
        t2 += casas
        t3 += ('V', ) * len(p_poss)
    return t1, t2, t3


#---------------------------------------------------------------------------------------------#
####################################FUNÇÕES ADICIONAIS#########################################
#---------------------------------------------------------------------------------------------#

def baralha_saco(seed):
    
    '''
    Baralha o conjunto após o ordenar numa lista
    Recebe o estado inicial do gerador pseudo-aleatório(seed), inteiro positivo,
    para a permutação.
    Contém o dicionário saco com o número de ocorrências das letras no saco
    do jogo de Scrabble
    Chama a função 'ordena_letras', para as ordenar numa lista;
    E chama a função 'permuta_letras' para as permutar
    Devolve a lista com as letras permutadas
    int -> list
    '''

    saco = {
            'A': 14, 'B': 3, 'C': 4, 'Ç': 2, 'D': 5, 'E': 11,
            'F': 2, 'G': 2, 'H': 2, 'I': 10, 'J': 2, 'L': 5,
            'M': 6, 'N': 4, 'O': 10, 'P': 4, 'Q': 1, 'R': 6,
            'S': 8, 'T': 5, 'U': 7, 'V': 2, 'X': 1, 'Z': 1 }
    
    letras_ordenadas = ordena_letras (ALFABETO, saco) 
    permuta_letras(letras_ordenadas, seed)
    return letras_ordenadas


def jogada_humano(tab, jog, vocab, pilha):
    
    '''
    Consoante o input, permite passar, trocar ou jogar no Scrabble
    Recebe o tabuleiro (tabuleiro), jog (jogador), o vocabulário (vocab) e a pilha (list)
    Até a jogada ser válida, pede ao jogador um input 'P', 'T' <seq_letras> 
    ou 'J' <linha> <coluna> <dir> <palavra>
    Se o input for 'P' (passar), a função devolve False e termina o ciclo
    Se o input começar por 'T' (trocar), a função vai analisar se a jogada é válida e se o for,
    troca as letras da palavra por letras da pilha, caso contrário pede um novo input
    Se o input começar por 'J' (jogar), a função analisa se a jogada é válida e se o for,
    joga as letras da palavra no tabuleiro e substitui-as por letras da pilha, 
    caso contrário pede um novo input
    Devolve False para a jogada 'passar' e True para as outras jogadas válidas
    tabuleiro, jogador, vocab, list -> bool
    '''
    
    while True:
        jogada_jogador=input(f"Jogada {jogador_identidade(jog)}: ").split() #transforma numa lista com os elementos sem os espaços
        conj_letras = jogador_letras(jog)
        if len (jogada_jogador) == 0:
            continue
        if jogada_jogador[0] == 'P' and len(jogada_jogador) == 1: 
            return False
        
        #T - Trocar
        elif jogada_jogador[0] == 'T': 
            palavra = ""
            for i in range (1,len(jogada_jogador),1): #concatena as letras a trocar numa palavra
                if jogada_jogador[i] in ALFABETO: 
                    palavra += jogada_jogador[i]
            
            if len (palavra) == 0: #Se nao conter caracteres válidos
                continue
            if len(palavra) > N_LETRAS_JOGADOR: #não trocar mais letras que as que se tem
                continue 
            if len(pilha) < len(palavra): #não trocar se ja nao houverem letras na pilha
                continue
            jog_teste=cria_duplicado_jog(jog)
            
            #copia apenas as letras, pq senao nao funciona, para testar em baixo para nao modificar destrutivamente
            pilha_teste=pilha.copy()
            if not elimina_let_substitui_conj(pilha_teste, jog_teste, palavra): #Assim, permite que não se troquem letras que não se tem
                continue
            elimina_let_substitui_conj(pilha, jog, palavra) #Só se modifica destrutivamente, depois de garantir que é válida
            return True
        
        #J - Jogar
        elif jogada_jogador[0] == 'J': 
            if len (jogada_jogador) != 5: #no caso de input inválido
                continue
            direcao = jogada_jogador[3]
            palavra = jogada_jogador[4]
            try:
                casa=cria_casa(int(jogada_jogador[1]),int(jogada_jogador[2]))
            except ValueError: #para nao parar o ciclo
                continue
            jogada = joga_palavra(tab, palavra, casa, direcao, conj_letras, vocab)
            if jogada == (): #se inválida, pede input outra vez
                continue 
            soma_pontos(jog, obtem_pontos(vocab, palavra))  #contagem dos pontos     
            if not elimina_let_substitui_conj(pilha, jog, jogada): #Dá-se novas letras ao jogador, pq já sabemos que é válida
                continue
            return True
        else:
            continue


def jogada_agente(tab, jog, vocab, pilha):
    
    '''
    Permite que o agente passe, troque ou jogue no Scrabble
    Recebe o tabuleiro (tabuleiro), jog (jogador), o vocabulário (vocab) e a pilha (list)
    Tenta jogar, se não o conseguir fazer tenta trocar todas as suas letras e se tal não
    for possível, passa a jogada. 
    Se a jogada for passar, a função devolve False e termina o ciclo
    Se a jogada for trocar, a função vai analisar se a jogada é válida e se o for,
    troca todas as letras do agente por letras da pilha, caso contrário, passa a jogada
    Se a jogada for jogar, a função analisa se a jogada é válida e se o for,
    joga as letras da palavra com mais pontuação, cnsoante a dificuldade escolhida
    e substitui-as por letras da pilha, caso contrário pede um novo input
    Devolve False para a jogada 'passar' e True para as outras jogadas válidas
    tabuleiro, jogador, vocab, list -> bool
    '''
    
    consegue_jogar = True
    consegue_trocar = True
    while True:
        
        conj_letras = jogador_letras(jog)
        
        #Passar
        if eh_tabuleiro_vazio(tab) or (consegue_jogar == False  and consegue_trocar == False):
            print(f"Jogada {jogador_identidade(jog)}: P")
            return False
        
        #Trocar
        elif consegue_jogar == False:
            if len(pilha) < N_LETRAS_JOGADOR:
                consegue_trocar = False
                continue
            else:
                conj_letras_espacado = " ".join(conj_letras)
                print(f"Jogada {jogador_identidade(jog)}: T {conj_letras_espacado}")
                elimina_let_substitui_conj(pilha, jog, conj_letras) 
                return True
            
        #Jogar
        else:
            if jogador_identidade(jog) == 'FACIL':
                N = 100
            elif jogador_identidade(jog) == 'MEDIO':
                N = 50
            else:
                N = 10
                        
            #fazer parecido ao procura palavra padrao
            melhor_pontuacao = 0
            melhor_palavra = None
            indice_melhor = None
            max_letras = numero_letras(jog)
            padroes, casas, dir = gera_todos_padroes(tab, max_letras)
            padroes_a_procurar=padroes[::N]
            casas_a_procurar=casas[::N]
            dir_a_procurar=dir[::N]
            for i in range (len(padroes_a_procurar)):
                par_atual = procura_palavra_padrao(vocab, padroes_a_procurar[i], conj_letras, melhor_pontuacao)
                pontos_atual = obtem_pontos_par(par_atual)
                if pontos_atual > melhor_pontuacao:
                    melhor_pontuacao = pontos_atual
                    melhor_palavra = obtem_palavra_par(par_atual)
                    indice_melhor = i
            if indice_melhor is not None:
                casa = casas_a_procurar[indice_melhor]
                direcao = dir_a_procurar[indice_melhor]
                jogada = joga_palavra(tab, melhor_palavra, casa, direcao, conj_letras, vocab)
                soma_pontos(jog, obtem_pontos(vocab, melhor_palavra))
                if not elimina_let_substitui_conj(pilha, jog, jogada): #Dá-se novas letras ao jogador, pq já sabemos que é válida
                    consegue_jogar = False
                    continue
                print(f"Jogada {jogador_identidade(jog)}: J {obtem_lin(casa)} {obtem_col(casa)} {direcao} {melhor_palavra}")
                return True
            else:
                consegue_jogar = False
                continue


def scrabble2(jogadores, nome_fich, seed):
    
    '''
    Permite jogar o jogo 'Scrabble2'
    A função recebe um tuplo com o nome dos jogadores humanos (cadeia de carateres não vazia)
    e o nível dos jogadores agentes (cadeia de carateres a começar por '@' seguido do nível) 
    na ordem em que jogam, um nome de ficheiro com o vocabulário e um inteiro positivo representando
    o estado inicial do gerador pseudo-aleatório.
    Valida os seus argumentos, e se forem válidos, entra num ciclo que só termina quando 
    já não houverem letras na pilha ou nos conjuntos dos jogadores ou quando todos os jogadores 
    passarem a jogada. Recorre à função 'ficheiro_para_vocabulário' para obter o vocabulário constituído 
    pelas palavras do ficheiro, 'baralha_saco' para baralhar as letras do saco, à 'distribui_letras', 
    para distribuir as letras do saco pelos jogadores, à 'cria_jogador', para os criar, 'eh_agente' para 
    verificar se o jogador é um agente, 'jogada_humano' e 'jogada_agente' para processar estas jogadas 
    e à função 'tabuleiro_para_str' e'jogador_para_str' para a representação visual do jogo.
    Devolve um tuplo com as pontuações dos jogadores no fim do jogo
    tuple, str, int -> tuple
    '''

    #Correção de argumentos
    if type(jogadores) != tuple:
        raise ValueError('scrabble2: argumentos inválidos')
    for jogador in jogadores:
        if type (jogador) != str:
            raise ValueError('scrabble2: argumentos inválidos')
        if jogador[0] == '@':
            if jogador in ('@FACIL', '@MEDIO', '@DIFICIL'):
                continue
            else:
                raise ValueError('scrabble2: argumentos inválidos')
        else:
            pass #nao é preciso ver se letras estão no alfabeto
            '''
            for letra in jogador.upper():
                if letra not in ALFABETO:
                    raise ValueError('scrabble2: argumentos inválidos')
            '''
    n_jogadores = len(jogadores)
    if (n_jogadores<N_MIN_JOGADORES or n_jogadores>N_MAX_JOGADORES):
        raise ValueError('scrabble2: argumentos inválidos')
    if type(seed) != int or seed<1:
        raise ValueError('scrabble2: argumentos inválidos')
    if type(nome_fich) != str:
        raise ValueError('scrabble2: argumentos inválidos')
    
    #criar o vocabulario
    vocab = ficheiro_para_vocabulario(nome_fich)
    #baralhar o saco de letras e dist. o conjunto de 7 letras pelos pelos jogadores em ordem
    saco = baralha_saco(seed)
    #lista dos jogadores e dos seus conjuntos
    lista_jogadores = []
    passou=0
    tab = cria_tabuleiro()
    print('Bem-vindo ao SCRABBLE2.')
    print(tabuleiro_para_str(tab))
    for i in range(0, len(jogadores)):
        #criar o jogador
        if jogadores[i] in ('@FACIL', '@MEDIO', '@DIFICIL'):
            novo_jogador = cria_agente(jogadores[i][1:])
        else:
            novo_jogador = cria_humano(jogadores[i])
        #dist as letras
        distribui_letras(novo_jogador, saco, N_LETRAS_JOGADOR)
        lista_jogadores.append(novo_jogador) #cria uma lista de dicionários, cada um representará um jogador
    while True:
        for k in range(0, n_jogadores): #Ciclo para cada jogada de cada jogador
            #loop dos jogadores
            for l in range(0, n_jogadores): #ciclo para cada jogador de cada jogada
                print(jogador_para_str(lista_jogadores[l]))
            
            #contagem das jogadas passadas, enquanto permite uma jogada qualquer (P, T, J)
            if eh_agente(lista_jogadores[k]):
                if jogada_agente(tab, lista_jogadores[k], vocab, saco) == False:
                    passou += 1 
                else:
                    passou = 0 #reincia o contador de jogadas passadas
            if eh_humano(lista_jogadores[k]):
                if jogada_humano(tab, lista_jogadores[k], vocab, saco) == False:
                    passou +=1
                else:
                    passou = 0
            resultado = () #reinciia o resultado a cada jogada, para o atualizar
            for i in range (0, n_jogadores):
                resultado += (jogador_pontos(lista_jogadores[i]), ) #atualiza o tuplo dos pontos
            if passou == n_jogadores:
                return resultado #se todos os jogadores passarem, termina
            if saco == [] and jogador_letras(lista_jogadores[k]) == []: #se saco vazio e jogador sem letras
                return resultado
            print(tabuleiro_para_str(tab))