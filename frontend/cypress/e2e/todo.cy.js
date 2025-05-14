
describe('Adding todo', () => {

    before(() => {
      return cy.fixture('user.json')
      .then((user) => {
        return cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          Cypress.env('uid', response.body._id.$oid)
          Cypress.env('name', user.firstName + ' ' + user.lastName)
          Cypress.env('email', user.email)
        })
      })
    })

    beforeEach(() => {
        const uid = Cypress.env('uid')
        const data = new FormData();
        data.append('title', "Test task");
        data.append('description', 'Task for test case');
        data.append('userid', uid);
        data.append('url', 'dQw4w9WgXcQ');
        data.append('todos', ['Watch video']);
        cy.log(data.toString())
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/tasks/create',
            form: false,
            body: data,
            encoding: 'binary'
        }).then((response) => {
            expect(response.status).to.equal(200)

            //Decode response from task
            const decoder = new TextDecoder('utf-8');
            const text = decoder.decode(response.body);
            const json = JSON.parse(text);
            const task = json[0]
            const taskId = task._id.$oid
            Cypress.env('taskid', taskId)

            cy.visit('http://localhost:3000/')
            cy.contains('div', 'Email Address')
                .find('input[type=text]')
                .type(Cypress.env('email'))
            cy.get('form')
                .submit()
        })
    })


    it('Leaving input of to-do empty should result in Add button being disabled', () => {
        cy.get('.container .container-element', {timeout: 10000})
            .contains('.title-overlay', 'Test task')
            .click()
        cy.get('ul.todo-list')
            .find('li')
            .last()
            .within(() => {
                cy.get('input[type=text]')
                    .clear()
                cy.get('input[type=submit]')
                    .should('have.attr', 'disabled')
                    .then((btn) => {
                        assert.isTrue(btn[0].disabled, 'Submit button should be disabled')
                    })
            })
        })

    it('Inputting in the form add pressing Add should result in to-do getting added', () => {
        cy.get('.container .container-element', {timeout: 10000})
            .contains('.title-overlay', 'Test task')
            .click()
        cy.get('ul.todo-list')
            .find('li')
            .last()
            .within(() => {
                cy.get('input[type=text]')
                    .type("Test to-do")
                cy.get('input[type=submit]')
                    .click()
            })
        cy.get('.todo-list').should('contain', 'Test to-do')
    })

    it('Clicking the checkbox while active should set to-do as done', () => {

        cy.get('.container .container-element', {timeout: 10000})
            .contains('.title-overlay', 'Test task')
            .click()
        cy.get('ul.todo-list')
            .within(() => {
                cy.contains('.todo-item', 'Watch video')
                    .find('.checker')
                    .click()
                cy.contains('.todo-item', 'Watch video')
                    .find('.checker')
                    .should('have.class', 'checked')
            })
    })

    it('Clicking the checkbox while done should set to-do as active', () => {
        const todoData = new FormData();
        todoData.append('taskid', Cypress.env('taskid'))
        todoData.append('done', true)
        todoData.append('description', 'Finished task');
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/todos/create',
            form: false,
            headers: { 'Cache-Control': 'no-cache' },
            body: todoData
        }).then((response) => {
            expect(response.status).to.equal(200)
            cy.get('.container .container-element', {timeout: 10000})
            .contains('.title-overlay', 'Test task')
            .click()
            cy.get('ul.todo-list')
                .within(() => {
                    cy.contains('.todo-item', 'Finished task')
                        .find('.checker')
                        .click()
                    cy.contains('.todo-item', 'Finished task')
                        .find('.checker')
                        .should('have.class', 'unchecked')
                })
        })
    })

    it('Clicking the X button should delete the to-do', () => {
        cy.intercept('DELETE', '**/todos/byid/**').as('deleteTodo')
        cy.get('.container .container-element', {timeout: 10000})
            .contains('.title-overlay', 'Test task')
            .click()
        cy.get('ul.todo-list')
            .within(() => {
                cy.contains('.todo-item', 'Watch video')
                    .get('.remover')
                    .click()

                })
        cy.wait(2000)
        cy.wait('@deleteTodo').then((interception) => { 
            cy.contains('.todo-item', 'Watch video')
                .should('not.exist')
        })
    })

    afterEach(() => {
        const uid = Cypress.env('uid')
        cy.request({
            method: 'GET',
            url: `http://localhost:5000/tasks/ofuser/${uid}`
        }).then((response) => {
            response.body.forEach((task) => {
                task.todos.forEach((todo) => {
                    cy.request({
                        method: 'DELETE',
                        url: `http://localhost:5000/todos/byid/${todo._id.$oid}`
                    })
                })
                cy.request({
                    method: 'DELETE',
                    url: `http://localhost:5000/tasks/byid/${task._id.$oid}`
                })
            })
            cy.log(response.body)
        })
    })

    after(() => {
        const uid = Cypress.env('uid')
        cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
        cy.log(response.body)
        })
    })

})