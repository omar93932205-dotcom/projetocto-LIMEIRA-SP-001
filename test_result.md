#====================================================================================================
# START - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================

# THIS SECTION CONTAINS CRITICAL TESTING INSTRUCTIONS FOR BOTH AGENTS
# BOTH MAIN_AGENT AND TESTING_AGENT MUST PRESERVE THIS ENTIRE BLOCK

# Communication Protocol:
# If the `testing_agent` is available, main agent should delegate all testing tasks to it.
#
# You have access to a file called `test_result.md`. This file contains the complete testing state
# and history, and is the primary means of communication between main and the testing agent.
#
# Main and testing agents must follow this exact format to maintain testing data. 
# The testing data must be entered in yaml format Below is the data structure:
# 
## user_problem_statement: {problem_statement}
## backend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.py"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## frontend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.js"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## metadata:
##   created_by: "main_agent"
##   version: "1.0"
##   test_sequence: 0
##   run_ui: false
##
## test_plan:
##   current_focus:
##     - "Task name 1"
##     - "Task name 2"
##   stuck_tasks:
##     - "Task name with persistent issues"
##   test_all: false
##   test_priority: "high_first"  # or "sequential" or "stuck_first"
##
## agent_communication:
##     -agent: "main"  # or "testing" or "user"
##     -message: "Communication message between agents"

# Protocol Guidelines for Main agent
#
# 1. Update Test Result File Before Testing:
#    - Main agent must always update the `test_result.md` file before calling the testing agent
#    - Add implementation details to the status_history
#    - Set `needs_retesting` to true for tasks that need testing
#    - Update the `test_plan` section to guide testing priorities
#    - Add a message to `agent_communication` explaining what you've done
#
# 2. Incorporate User Feedback:
#    - When a user provides feedback that something is or isn't working, add this information to the relevant task's status_history
#    - Update the working status based on user feedback
#    - If a user reports an issue with a task that was marked as working, increment the stuck_count
#    - Whenever user reports issue in the app, if we have testing agent and task_result.md file so find the appropriate task for that and append in status_history of that task to contain the user concern and problem as well 
#
# 3. Track Stuck Tasks:
#    - Monitor which tasks have high stuck_count values or where you are fixing same issue again and again, analyze that when you read task_result.md
#    - For persistent issues, use websearch tool to find solutions
#    - Pay special attention to tasks in the stuck_tasks list
#    - When you fix an issue with a stuck task, don't reset the stuck_count until the testing agent confirms it's working
#
# 4. Provide Context to Testing Agent:
#    - When calling the testing agent, provide clear instructions about:
#      - Which tasks need testing (reference the test_plan)
#      - Any authentication details or configuration needed
#      - Specific test scenarios to focus on
#      - Any known issues or edge cases to verify
#
# 5. Call the testing agent with specific instructions referring to test_result.md
#
# IMPORTANT: Main agent must ALWAYS update test_result.md BEFORE calling the testing agent, as it relies on this file to understand what to test next.

#====================================================================================================
# END - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================



#====================================================================================================
# Testing Data - Main Agent and testing sub agent both should log testing data below this section
#====================================================================================================

user_problem_statement: "Popular o painel administrativo (SEAP-MA) com 150 inscrições de teste realistas, com fotos reais, vagas aleatórias entre os 9 cargos, metade em desktop e metade em mobile."

backend:
  - task: "Seed de 150 inscrições realistas (script /app/scripts/seed_inscricoes.py)"
    implemented: true
    working: true
    file: "/app/scripts/seed_inscricoes.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
        -working: "NA"
        -agent: "main"
        -comment: "Script inseriu 150 inscrições (75 desktop / 75 mobile), 80 retratos reais (randomuser.me) usados como doc_frente/doc_verso em cadastros.form_data, vagas aleatórias entre os 9 cargos (codigos 01-09), + 220 acessos extras para funil realista. Precisa validar via API admin autenticada."
        -working: true
        -agent: "testing"
        -comment: "Validado via API admin. Resultados: 152 inscrições finalizadas (77 desktop / 75 mobile), 381 acessos totais, 151 cadastros com documentos. Distribuição de cargos: todos os 9 cargos presentes com valores corretos (Inspetor=150.0, Monitor=85.0, Especialidades superiores=180.0, Técnicos=120.0). Fotos reais confirmadas (11.5KB JPEG). Todos os campos obrigatórios presentes (nome, cpf 11 dígitos, email, concurso contendo 'Administração Penitenciária do Maranhão')."

  - task: "API admin retorna inscrições e documentos corretamente"
    implemented: true
    working: true
    file: "/app/backend/admin_routes.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
        -working: "NA"
        -agent: "main"
        -comment: "Endpoints a validar: POST /api/admin/auth/login (donas/Seinao10@@); GET /api/admin/inscriptions (>=150 finalized, campos device desktop/mobile, cargo_titulo, valor); GET /api/admin/dashboard/kpis; GET /api/admin/documentos e GET /api/admin/documentos/{cpf}/{tipo}?token= (retorna imagem)."
        -working: true
        -agent: "testing"
        -comment: "Todos os endpoints validados com sucesso: 1) POST /api/admin/auth/login retorna 200 com token JWT e user.username='donas' ✓; 2) GET /api/admin/inscriptions retorna 152 inscrições finalizadas com device mix balanceado (77 desktop, 75 mobile), todos os 9 cargo_titulo presentes, valores corretos por cargo ✓; 3) GET /api/admin/dashboard/kpis retorna inscricoes=152 e acessos=381 ✓; 4) GET /api/admin/documentos retorna 151 items com total>0 ✓; 5) GET /api/admin/documentos/{cpf}/frente?token=<jwt> retorna HTTP 200 com Content-Type: image/jpeg (11533 bytes) ✓; 6) GET /api/admin/inscriptions sem Authorization retorna 401 ✓. Taxa de sucesso: 100% (6/6 testes)."

metadata:
  created_by: "main_agent"
  version: "1.0"
  test_sequence: 2
  run_ui: false

test_plan:
  current_focus:
    - "Seed de 150 inscrições realistas (script /app/scripts/seed_inscricoes.py)"
    - "API admin retorna inscrições e documentos corretamente"
  stuck_tasks: []
  test_all: false
  test_priority: "high_first"

agent_communication:
    -agent: "main"
    -message: "Rodei o seed de 150 inscrições no MongoDB. Por favor valide via API admin: 1) login /api/admin/auth/login com donas/Seinao10@@ retorna token; 2) GET /api/admin/inscriptions com Bearer token retorna total>=150 finalizadas, com mix de device (desktop e mobile), cargo_titulo entre os 9 cargos e valor correspondente (Inspetor=150, Monitor=85, Especialista/Especialidade sociais=180, Assistente/Técnico=120); 3) GET /api/admin/dashboard/kpis mostra inscricoes>=150 e acessos>=150; 4) GET /api/admin/documentos lista candidatos com documentos e GET /api/admin/documentos/{cpf}/{tipo}?token=<jwt> devolve uma imagem (content-type image/*). Não teste UI, apenas backend/API."
    -agent: "testing"
    -message: "Validação completa realizada com sucesso. Criado /app/backend_test.py com 6 testes abrangentes. Resultados: ✅ Todos os 6 testes passaram (100% sucesso). Detalhes: 152 inscrições finalizadas (2 a mais que o esperado, provavelmente de testes anteriores), device mix balanceado (77 desktop/75 mobile ≈50/50), todos os 9 cargos presentes com valores corretos, 381 acessos totais (150 inscrições + 220 extras + alguns de testes), 151 cadastros com documentos (fotos reais JPEG), endpoint de imagem retorna Content-Type: image/jpeg com 11.5KB, autenticação JWT funcionando corretamente, proteção de rotas funcionando (401 sem token). Nenhum problema crítico encontrado. Backend está 100% funcional conforme especificação."