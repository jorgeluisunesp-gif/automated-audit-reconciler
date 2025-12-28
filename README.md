# **📊 Automated Audit Reconciler**

Ferramenta de auditoria digital que automatiza a conciliação entre Extratos Bancários e Razão Contábil, identificando divergências financeiras, omissões e lançamentos sem lastro com precisão decimal.

## **🎯 Objetivo de Negócio**

No contexto de **Auditoria Contábil e Fiscal**, a validação cruzada de dados (*Cross-Checking*) é uma das tarefas mais críticas e demoradas. Este projeto visa eliminar o erro humano e reduzir o tempo de fechamento contábil, transformando horas de conferência manual em segundos de processamento computacional.

**Ideal para:**

* Departamentos de Controle Interno.  
* Escritórios de Contabilidade (BPO Financeiro).  
* Auditoria de prestações de contas públicas.

## **🚀 Funcionalidades**

* **Simulação de Cenários (Mock Data):** Gera automaticamente dados fictícios de bancos e sistemas ERP contendo erros propositais (omissões, valores divergentes) para teste de integridade.  
* **Algoritmo de Reconciliação:** Utiliza *Full Outer Joins* para garantir que nenhuma transação seja perdida, independente da origem.  
* **Detecção de Tipologias de Erro:**  
  * 🔴 **Omissão Contábil:** Dinheiro saiu do banco mas não foi registrado.  
  * 🟠 **Sem Lastro:** Registrado no sistema mas sem movimentação bancária correspondente.  
  * 🟡 **Divergência de Valor:** Erros de digitação ou retenções não lançadas.  
* **Relatórios Executivos:** Exportação automática para Excel (.xlsx) pronto para apresentação.

## **🛠️ Tecnologias**

* **Python 3:** Linguagem core.  
* **Pandas & NumPy:** Manipulação vetorial de dados financeiros.  
* **OpenPyXL:** Geração de relatórios compatíveis com Excel.

## **⚙️ Como Executar**

1. **Clone o repositório**  
   git clone \[https://github.com/jorgeluisunesp-gif/automated-audit-reconciler.git\](https://github.com/jorgeluisunesp-gif/automated-audit-reconciler.git)

2. **Instale as dependências**  
   pip install \-r requirements.txt

3. **Execute a Auditoria**  
   python main.py

   *Nota: Na primeira execução, o sistema detectará a ausência de dados e gerará arquivos CSV de teste automaticamente.*  
4. Analise o Resultado  
   Abra o arquivo Relatorio\_Auditoria\_Divergencias.xlsx gerado na raiz do projeto.

## **📄 Licença**

Distribuído sob a licença MIT. Projeto desenvolvido para portfólio de Ciência de Dados aplicada a Finanças.