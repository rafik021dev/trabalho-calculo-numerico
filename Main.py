import math

def main():
    print("=== Cálculo da velocidade ótima de exaustão dos gases ===")

    variacao_velocidade = float(input("Digite a variação de velocidade (Δv, m/s): "))
    tempo_operacao = float(input("Digite o tempo total de operação (s): "))
    coeficiente_combustivel = float(input("Digite o coeficiente α (kg/W): "))

     # Função para calcular a razão das massas
    def razao_massas(velocidade_exaustao):
        termo_exp = math.exp(-variacao_velocidade / velocidade_exaustao)
        return termo_exp - (coeficiente_combustivel * velocidade_exaustao**2) / (2 * tempo_operacao) * (1 - termo_exp)

    def derivada(funcao, ponto, passo=1e-3):
        return (funcao(ponto + passo) - funcao(ponto - passo)) / (2 * passo)

    def derivada_razao_massas(velocidade_exaustao):
        return derivada(razao_massas, velocidade_exaustao)

    # Método da bisseção
    def metodo_bissecao(funcao, a, b, tolerancia=1e-6, max_iter=100):
        f_a = funcao(a)
        f_b = funcao(b)
        if f_a * f_b > 0:
            raise ValueError("O intervalo não contém uma mudança de sinal.")
        for _ in range(max_iter):
            meio = (a + b) / 2
            f_meio = funcao(meio)
            if abs(f_meio) < tolerancia or (b - a) / 2 < tolerancia:
                return meio
            if f_a * f_meio < 0:
                b = meio
                f_b = f_meio
            else:
                a = meio
                f_a = f_meio
        return (a + b) / 2

    # Intervalo inicial
    limite_inferior = float(input("Digite o limite inferior para v (m/s): "))
    limite_superior = float(input("Digite o limite superior para v (m/s): "))

    passo_scan = (limite_superior - limite_inferior) / 100
    subintervalo = None
    anterior = derivada_razao_massas(limite_inferior)

    for v in [limite_inferior + i * passo_scan for i in range(1, 101)]:
        atual = derivada_razao_massas(v)
        if anterior * atual < 0:
            subintervalo = (v - passo_scan, v)
            break
        anterior = atual

    if subintervalo is None:
        print("\nNenhuma mudança de sinal detectada no intervalo informado.")
        print("Tente ampliar o intervalo (ex: 500 até 10000 m/s).")
        return

    a, b = subintervalo
    v_otimo = metodo_bissecao(derivada_razao_massas, a, b)
    print(f"\nVelocidade ótima de exaustão: {v_otimo:.4f} m/s")
    print(f"Razão mínima Mf/M0: {razao_massas(v_otimo):.6f}")

if __name__ == "__main__":
    main()
