// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
Cypress.Commands.add('login', () => {
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user
    cy.fixture('user.json')
        .then((user) => {
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/users/create',
                form: true,
                body: user
            }).then((response) => {
                uid = response.body._id.$oid
                name = user.firstName + ' ' + user.lastName
                email = user.email
   
                cy.visit('http://localhost:3000')
            
                cy.contains('div', 'Email Address')
                  .find('input[type=text]')
                  .type(email)
                // alternative, imperative way of detecting that input field
                //cy.get('.inputwrapper #email')
                //    .type(email)
            
                // submit the form on this page
                cy.get('form')
                  .submit()
            
                // assert that the user is now logged in
                cy.get('h1')
                  .should('contain.text', 'Your tasks, ' + name)
                return uid
            })
        })
})

Cypress.Commands.add('delUser', (uid) => {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
})



//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })