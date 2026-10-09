/* Códigos da apostila: cada etapa tem fase, título, descrição e arquivos. */
const STEPS = {
  github: {
    fase: 'Ambiente · etapa 1', titulo: 'Repositório no GitHub',
    desc: 'Crie o repositório vazio no GitHub (sem README) e copie a URL. Ela liga o projeto local ao remoto.',
    files: [
      { nome: 'URL do repositório', lang: 'plaintext', code:
'https://github.com/seu-usuario/sistema-usuarios.git' }
    ]
  },

  projeto: {
    fase: 'Ambiente · etapa 2', titulo: 'Criar o projeto Angular',
    desc: 'Gera a estrutura base, conecta ao GitHub e sobe o servidor de desenvolvimento.',
    files: [
      { nome: 'terminal · criar', lang: 'bash', code:
'ng new sistema-usuarios\n# Stylesheet: CSS\n# Routing: Yes\n\ncd sistema-usuarios' },
      { nome: 'terminal · git', lang: 'bash', code:
'git remote add origin https://github.com/seu-usuario/sistema-usuarios.git\ngit add .\ngit commit -m "Projeto Angular 20 criado"\ngit branch -M main\ngit push -u origin main' },
      { nome: 'terminal · rodar', lang: 'bash', code:
'ng serve\n# abra http://localhost:4200' }
    ]
  },

  bootstrap: {
    fase: 'Ambiente · etapa 3', titulo: 'Instalar o Bootstrap',
    desc: 'Instala o pacote e importa o CSS global para liberar as classes em todo o projeto.',
    files: [
      { nome: 'terminal', lang: 'bash', code: 'npm install bootstrap' },
      { nome: 'src/styles.css', lang: 'css', code:
"@import 'bootstrap/dist/css/bootstrap.min.css';" },
      { nome: 'angular.json (opcional: JS)', lang: 'json', code:
'"architect": {\n  "build": {\n    "options": {\n      "styles": ["src/styles.css"],\n      "scripts": [\n        "node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"\n      ]\n    }\n  }\n}' }
    ]
  },

  componente: {
    fase: 'Estrutura · etapa 4', titulo: 'Componente Cadastro',
    desc: 'O CLI cria a pasta do componente com lógica, template, estilo e teste.',
    files: [
      { nome: 'terminal', lang: 'bash', code:
'ng generate component cadastro\n# ou, abreviado:\nng g c cadastro' },
      { nome: 'pasta gerada', lang: 'plaintext', code:
'src/app/cadastro/\n├── cadastro.ts\n├── cadastro.html\n├── cadastro.css\n└── cadastro.spec.ts' }
    ]
  },

  formulario: {
    fase: 'Estrutura · etapa 5', titulo: 'Formulário em HTML',
    desc: 'Template do Cadastro só com HTML e classes do Bootstrap. Ainda não salva dados.',
    files: [
      { nome: 'src/app/cadastro/cadastro.html', lang: 'html', code:
'<div class="container mt-5">\n' +
'  <div class="row justify-content-center">\n' +
'    <div class="col-md-8 col-lg-6">\n' +
'      <div class="card shadow">\n' +
'        <div class="card-body">\n' +
'          <h2 class="text-center mb-4">Cadastro de Usuário</h2>\n\n' +
'          <form>\n' +
'            <div class="mb-3">\n' +
'              <label for="nome" class="form-label">Nome completo</label>\n' +
'              <input type="text" class="form-control" id="nome" placeholder="Digite seu nome completo" />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="email" class="form-label">E-mail</label>\n' +
'              <input type="email" class="form-control" id="email" placeholder="Digite seu e-mail" />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="senha" class="form-label">Senha</label>\n' +
'              <input type="password" class="form-control" id="senha" placeholder="Digite sua senha" />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="telefone" class="form-label">Telefone</label>\n' +
'              <input type="text" class="form-control" id="telefone" placeholder="Digite seu telefone" />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="dataNascimento" class="form-label">Data de nascimento</label>\n' +
'              <input type="date" class="form-control" id="dataNascimento" />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="endereco" class="form-label">Endereço</label>\n' +
'              <input type="text" class="form-control" id="endereco" placeholder="Digite seu endereço" />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="cidade" class="form-label">Cidade</label>\n' +
'              <input type="text" class="form-control" id="cidade" placeholder="Digite sua cidade" />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="estado" class="form-label">Estado</label>\n' +
'              <select class="form-select" id="estado">\n' +
'                <option selected>Selecione</option>\n' +
'                <option>RJ</option>\n' +
'                <option>SP</option>\n' +
'                <option>MG</option>\n' +
'                <option>ES</option>\n' +
'              </select>\n' +
'            </div>\n\n' +
'            <div class="d-grid">\n' +
'              <button type="submit" class="btn btn-primary">Cadastrar</button>\n' +
'            </div>\n' +
'          </form>\n' +
'        </div>\n' +
'      </div>\n' +
'    </div>\n' +
'  </div>\n' +
'</div>' }
    ]
  },

  app: {
    fase: 'Estrutura · etapa 6', titulo: 'App chama o Cadastro',
    desc: 'Importa a classe Cadastro no App e usa o seletor app-cadastro no template principal.',
    files: [
      { nome: 'src/app/app.ts', lang: 'typescript', code:
"import { Component } from '@angular/core';\nimport { Cadastro } from './cadastro/cadastro';\n\n@Component({\n  selector: 'app-root',\n  imports: [Cadastro],\n  templateUrl: './app.html',\n  styleUrl: './app.css'\n})\nexport class App {\n  title = 'sistema-usuarios';\n}" },
      { nome: 'src/app/app.html', lang: 'html', code:
'<app-cadastro></app-cadastro>' }
    ]
  },

  service: {
    fase: 'Evolução CRUD · etapa 7', titulo: 'Service de usuários',
    desc: 'Modelo Usuario + UsuarioService compartilhado (providedIn root) para listar, adicionar e remover.',
    files: [
      { nome: 'terminal · modelo', lang: 'bash', code:
'ng g interface models/usuario' },
      { nome: 'src/app/models/usuario.ts', lang: 'typescript', code:
'export interface Usuario {\n  id: number;\n  nome: string;\n  email: string;\n  senha: string;\n  telefone: string;\n  dataNascimento: string;\n  endereco: string;\n  cidade: string;\n  estado: string;\n}' },
      { nome: 'terminal · service', lang: 'bash', code:
'ng g service services/usuario-service' },
      { nome: 'src/app/services/usuario-service.ts', lang: 'typescript', code:
"import { Injectable } from '@angular/core';\nimport { Usuario } from '../models/usuario';\n\n@Injectable({ providedIn: 'root' })\nexport class UsuarioService {\n  private usuarios: Usuario[] = [];\n  private proximoId = 1;\n\n  listar(): Usuario[] {\n    return this.usuarios;\n  }\n\n  adicionar(dados: Omit<Usuario, 'id'>): void {\n    this.usuarios.push({ id: this.proximoId++, ...dados });\n  }\n\n  remover(id: number): void {\n    this.usuarios = this.usuarios.filter(u => u.id !== id);\n  }\n}" }
    ]
  },

  binding: {
    fase: 'Evolução CRUD · etapa 8', titulo: 'Bindings no formulário',
    desc: 'FormsModule + [(ngModel)] em cada campo e (ngSubmit) chamando salvar() no service.',
    files: [
      { nome: 'src/app/cadastro/cadastro.ts', lang: 'typescript', code:
"import { Component, inject } from '@angular/core';\nimport { FormsModule } from '@angular/forms';\nimport { Router } from '@angular/router';\nimport { UsuarioService } from '../services/usuario-service';\n\n@Component({\n  selector: 'app-cadastro',\n  imports: [FormsModule],\n  templateUrl: './cadastro.html',\n  styleUrl: './cadastro.css'\n})\nexport class Cadastro {\n  private service = inject(UsuarioService);\n  private router = inject(Router);\n\n  usuario = {\n    nome: '', email: '', senha: '', telefone: '',\n    dataNascimento: '', endereco: '', cidade: '', estado: ''\n  };\n\n  salvar(): void {\n    this.service.adicionar({ ...this.usuario });\n    this.router.navigate(['/lista']);\n  }\n}" },
      { nome: 'src/app/cadastro/cadastro.html', lang: 'html', code:
'<div class="container mt-5">\n' +
'  <div class="row justify-content-center">\n' +
'    <div class="col-md-8 col-lg-6">\n' +
'      <div class="card shadow">\n' +
'        <div class="card-body">\n' +
'          <h2 class="text-center mb-4">Cadastro de Usuário</h2>\n\n' +
'          <form (ngSubmit)="salvar()" #form="ngForm">\n' +
'            <div class="mb-3">\n' +
'              <label for="nome" class="form-label">Nome completo</label>\n' +
'              <input type="text" class="form-control" id="nome" name="nome"\n' +
'                     [(ngModel)]="usuario.nome" required />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="email" class="form-label">E-mail</label>\n' +
'              <input type="email" class="form-control" id="email" name="email"\n' +
'                     [(ngModel)]="usuario.email" required />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="senha" class="form-label">Senha</label>\n' +
'              <input type="password" class="form-control" id="senha" name="senha"\n' +
'                     [(ngModel)]="usuario.senha" />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="telefone" class="form-label">Telefone</label>\n' +
'              <input type="text" class="form-control" id="telefone" name="telefone"\n' +
'                     [(ngModel)]="usuario.telefone" />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="dataNascimento" class="form-label">Data de nascimento</label>\n' +
'              <input type="date" class="form-control" id="dataNascimento" name="dataNascimento"\n' +
'                     [(ngModel)]="usuario.dataNascimento" />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="endereco" class="form-label">Endereço</label>\n' +
'              <input type="text" class="form-control" id="endereco" name="endereco"\n' +
'                     [(ngModel)]="usuario.endereco" />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="cidade" class="form-label">Cidade</label>\n' +
'              <input type="text" class="form-control" id="cidade" name="cidade"\n' +
'                     [(ngModel)]="usuario.cidade" />\n' +
'            </div>\n\n' +
'            <div class="mb-3">\n' +
'              <label for="estado" class="form-label">Estado</label>\n' +
'              <select class="form-select" id="estado" name="estado" [(ngModel)]="usuario.estado">\n' +
'                <option value="">Selecione</option>\n' +
'                <option>RJ</option>\n' +
'                <option>SP</option>\n' +
'                <option>MG</option>\n' +
'                <option>ES</option>\n' +
'              </select>\n' +
'            </div>\n\n' +
'            <!-- prévia ao vivo: interpolação -->\n' +
'            @if (usuario.nome) {\n' +
'              <p class="text-muted">Cadastrando: {{ usuario.nome }}</p>\n' +
'            }\n\n' +
'            <div class="d-grid">\n' +
'              <!-- property binding: desativa enquanto o form é inválido -->\n' +
'              <button type="submit" class="btn btn-primary" [disabled]="form.invalid">\n' +
'                Cadastrar\n' +
'              </button>\n' +
'            </div>\n' +
'          </form>\n' +
'        </div>\n' +
'      </div>\n' +
'    </div>\n' +
'  </div>\n' +
'</div>' }
    ]
  },

  lista: {
    fase: 'Evolução CRUD · etapa 9', titulo: 'Componente Lista',
    desc: 'Lê os usuários do service e mostra numa tabela com @if, @for e botão de excluir.',
    files: [
      { nome: 'terminal', lang: 'bash', code: 'ng g c lista' },
      { nome: 'src/app/lista/lista.ts', lang: 'typescript', code:
"import { Component, inject } from '@angular/core';\nimport { RouterLink } from '@angular/router';\nimport { UsuarioService } from '../services/usuario-service';\n\n@Component({\n  selector: 'app-lista',\n  imports: [RouterLink],\n  templateUrl: './lista.html',\n  styleUrl: './lista.css'\n})\nexport class Lista {\n  private service = inject(UsuarioService);\n\n  get usuarios() {\n    return this.service.listar();\n  }\n\n  remover(id: number): void {\n    this.service.remover(id);\n  }\n}" },
      { nome: 'src/app/lista/lista.html', lang: 'html', code:
'<div class="container mt-5">\n' +
'  <div class="d-flex justify-content-between align-items-center mb-3">\n' +
'    <h2>Usuários cadastrados</h2>\n' +
'    <a routerLink="/cadastro" class="btn btn-primary">Novo usuário</a>\n' +
'  </div>\n\n' +
'  @if (usuarios.length > 0) {\n' +
'    <p class="text-muted">{{ usuarios.length }} usuário(s) encontrado(s)</p>\n' +
'  }\n\n' +
'  <table class="table table-striped align-middle">\n' +
'    <thead>\n' +
'      <tr>\n' +
'        <th>Nome</th><th>E-mail</th><th>Telefone</th><th>Cidade/UF</th><th></th>\n' +
'      </tr>\n' +
'    </thead>\n' +
'    <tbody>\n' +
'      @for (u of usuarios; track u.id) {\n' +
'        <tr>\n' +
'          <td>{{ u.nome }}</td>\n' +
'          <td>{{ u.email }}</td>\n' +
'          <td>{{ u.telefone }}</td>\n' +
'          <td>{{ u.cidade }}/{{ u.estado }}</td>\n' +
'          <td class="text-end">\n' +
'            <button class="btn btn-sm btn-outline-danger" (click)="remover(u.id)">\n' +
'              Excluir\n' +
'            </button>\n' +
'          </td>\n' +
'        </tr>\n' +
'      } @empty {\n' +
'        <tr>\n' +
'          <td colspan="5" class="text-center text-muted">Nenhum usuário cadastrado.</td>\n' +
'        </tr>\n' +
'      }\n' +
'    </tbody>\n' +
'  </table>\n' +
'</div>' }
    ]
  },

  rotas: {
    fase: 'Evolução CRUD · etapa 10', titulo: 'Rotas',
    desc: 'Cada URL abre um componente dentro do router-outlet; o menu navega com routerLink.',
    files: [
      { nome: 'src/app/app.routes.ts', lang: 'typescript', code:
"import { Routes } from '@angular/router';\nimport { Cadastro } from './cadastro/cadastro';\nimport { Lista } from './lista/lista';\n\nexport const routes: Routes = [\n  { path: '', redirectTo: 'cadastro', pathMatch: 'full' },\n  { path: 'cadastro', component: Cadastro },\n  { path: 'lista', component: Lista },\n  { path: '**', redirectTo: 'cadastro' }\n];" },
      { nome: 'src/app/app.config.ts', lang: 'typescript', code:
"import { ApplicationConfig } from '@angular/core';\nimport { provideRouter } from '@angular/router';\nimport { routes } from './app.routes';\n\nexport const appConfig: ApplicationConfig = {\n  providers: [\n    // ...outros providers gerados pelo CLI\n    provideRouter(routes)\n  ]\n};" },
      { nome: 'src/app/app.ts', lang: 'typescript', code:
"import { Component } from '@angular/core';\nimport { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';\n\n@Component({\n  selector: 'app-root',\n  imports: [RouterOutlet, RouterLink, RouterLinkActive],\n  templateUrl: './app.html',\n  styleUrl: './app.css'\n})\nexport class App {\n  title = 'sistema-usuarios';\n}" },
      { nome: 'src/app/app.html', lang: 'html', code:
'<nav class="navbar navbar-expand bg-dark" data-bs-theme="dark">\n' +
'  <div class="container">\n' +
'    <span class="navbar-brand">Sistema de Usuários</span>\n' +
'    <div class="navbar-nav">\n' +
'      <a class="nav-link" routerLink="/cadastro" routerLinkActive="active">Cadastro</a>\n' +
'      <a class="nav-link" routerLink="/lista" routerLinkActive="active">Lista</a>\n' +
'    </div>\n' +
'  </div>\n' +
'</nav>\n\n' +
'<!-- aqui aparece o componente da rota atual -->\n' +
'<router-outlet />' }
    ]
  },

  estrutura: {
    fase: 'Resumo', titulo: 'Estrutura final',
    desc: 'Pastas e arquivos de src/app ao fim das 10 etapas.',
    files: [
      { nome: 'src/app', lang: 'plaintext', code:
'src/\n├── styles.css            ← import do Bootstrap\n└── app/\n    ├── cadastro/\n    │   ├── cadastro.html\n    │   ├── cadastro.css\n    │   ├── cadastro.spec.ts\n    │   └── cadastro.ts\n    ├── lista/\n    │   ├── lista.html\n    │   ├── lista.css\n    │   ├── lista.spec.ts\n    │   └── lista.ts\n    ├── models/\n    │   └── usuario.ts\n    ├── services/\n    │   ├── usuario-service.spec.ts\n    │   └── usuario-service.ts\n    ├── app.config.ts\n    ├── app.routes.ts\n    ├── app.html\n    ├── app.css\n    ├── app.spec.ts\n    └── app.ts' }
    ]
  },

  exercicio: {
    fase: 'Exercício', titulo: 'Duas colunas com grid',
    desc: 'Trecho de solução: campos dentro de row, cada um com col-md-6.',
    files: [
      { nome: 'trecho do cadastro.html', lang: 'html', code:
'<h5 class="mt-4 mb-3">Endereço</h5>\n' +
'<div class="row g-3">\n' +
'  <div class="col-md-6">\n' +
'    <label for="cep" class="form-label">CEP</label>\n' +
'    <input type="text" class="form-control" id="cep" name="cep" [(ngModel)]="usuario.cep" />\n' +
'  </div>\n' +
'  <div class="col-md-6">\n' +
'    <label for="bairro" class="form-label">Bairro</label>\n' +
'    <input type="text" class="form-control" id="bairro" name="bairro" [(ngModel)]="usuario.bairro" />\n' +
'  </div>\n' +
'</div>\n\n' +
'<h5 class="mt-4 mb-3">Contatos</h5>\n' +
'<div class="row g-3">\n' +
'  <div class="col-md-6">\n' +
'    <label for="celular" class="form-label">Celular</label>\n' +
'    <input type="tel" class="form-control" id="celular" name="celular" [(ngModel)]="usuario.celular" />\n' +
'  </div>\n' +
'  <div class="col-md-6">\n' +
'    <label for="instagram" class="form-label">Instagram</label>\n' +
'    <input type="text" class="form-control" id="instagram" name="instagram" [(ngModel)]="usuario.instagram" />\n' +
'  </div>\n' +
'</div>' }
    ]
  }
};
