/*! jQuery Validation Plugin - v1.19.0 - 11/28/2018
 * https://jqueryvalidation.org/
 * Copyright (c) 2018 Jörn Zaefferer; Licensed MIT */
!function(a){"function"==typeof define&&define.amd?define(["jquery","../jquery.validate.min"],a):"object"==typeof module&&module.exports?module.exports=a(require("jquery")):a(jQuery)}(function(a){return a.extend(a.validator.messages,{required:"Campo obbligatorio",remote:"Controlla questo campo",email:"Inserisci un indirizzo email valido",url:"Inserisci un indirizzo web valido",date:"Inserisci una data valida",dateISO:"Inserisci una data valida (ISO)",number:"Inserisci un numero valido",digits:"Inserisci solo numeri",creditcard:"Inserisci un numero di carta di credito valido",equalTo:"Il valore non corrisponde",extension:"Inserisci un valore con un&apos;estensione valida",maxlength:a.validator.format("Non inserire pi&ugrave; di {0} caratteri"),minlength:a.validator.format("Inserisci almeno {0} caratteri"),rangelength:a.validator.format("Inserisci un valore compreso tra {0} e {1} caratteri"),range:a.validator.format("Inserisci un valore compreso tra {0} e {1}"),max:a.validator.format("Inserisci un valore minore o uguale a {0}"),min:a.validator.format("Inserisci un valore maggiore o uguale a {0}"),nifES:"Inserisci un NIF valido",nieES:"Inserisci un NIE valido",cifES:"Inserisci un CIF valido",currency:"Inserisci una valuta valida"}),a});