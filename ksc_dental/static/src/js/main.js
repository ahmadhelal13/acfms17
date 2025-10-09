// odoo.define('web.web_client', function (require) {
//     'use strict';

//     const AbstractService = require('web.AbstractService');
//     const env = require('web.env');
//     const WebClient = require('web.AbstractWebClient');
//     const Registries = require('ksc_dental.Registries');

//     const DentalView = require('ksc_dental.DentalView');

//     const { configureGui } = require('ksc_dental.Gui');

//     owl.config.mode = env.isDebug() ? 'dev' : 'prod';
//     owl.Component.env = env;

//     Registries.Component.add(owl.misc.Portal);

//     async function startPosApp(webClient) {
//         Registries.Component.freeze();
//         await env.session.is_bound;
//         env.qweb.addTemplates(env.session.owlTemplates);
//         env.bus = new owl.core.EventBus();
//         await owl.utils.whenReady();
//         await webClient.setElement(document.body);
//         await webClient.start();
//         webClient.isStarted = true;
//         const dentalView = new (Registries.Component.get(DentalView))(null, { webClient });
//         await dentalView.mount(document.querySelector('.o_action_manager'));
//         configureGui({ component: DentalView });
//         await dentalView.willUnmount();
//     }

//     AbstractService.prototype.deployServices(env);
//     const webClient = new WebClient();
//     startPosApp(webClient);
//     return webClient;
// });
