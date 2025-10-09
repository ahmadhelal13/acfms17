// odoo.define('ksc_dental.ComponentRegistry', function(require) {
//     'use strict';

//     const DentalComponent = require('ksc_dental.DentalComponent');
//     const ClassRegistry = require('ksc_dental.ClassRegistry');

//     class ComponentRegistry extends ClassRegistry {
//         freeze() {
//             super.freeze();
//             // Make sure DentalComponent has the compiled classes.
//             // This way, we don't need to explicitly declare that
//             // a set of components is children of another.
//             DentalComponent.components = {};
//             for (let [base, compiledClass] of this.cache.entries()) {
//                 DentalComponent.components[base.name] = compiledClass;
//             }
//         }
//         _recompute(base, old) {
//             const res = super._recompute(base, old);
//             if (typeof base === 'string') {
//                 base = this.baseNameMap[base];
//             }
//             DentalComponent.components[base.name] = res;
//             return res;
//         }
//     }

//     return ComponentRegistry;
// });
