// odoo.define('ksc_dental.Gui', function (require) {
//     'use strict';

//     const config = {};
//     const configureGui = ({ component }) => {
//         config.component = component;
//         config.availableMethods = new Set([
//             'showPopup',
//             'showTempScreen',
//             'playSound',
//             'setSyncStatus',
//         ]);
//     };
//     const Gui = new Proxy(config, {
//         get(target, key) {
//             const { component, availableMethods } = target;
//             if (!component) throw new Error(`Call 'configureGui' before using Gui.`);
//             const isMounted = component.__owl__.status === 3 /* mounted */;
//             if (availableMethods.has(key) && isMounted) {
//                 return component[key].bind(component);
//             }
//         },
//     });

//     return { configureGui, Gui };
// });
