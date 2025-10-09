// /** @odoo-module **/

// import { patch } from "@web/core/utils/patch";
// import { ImageField } from "@web/views/fields/image/image_field";
// import { _t } from "@web/core/l10n/translation";
// import { Dialog } from "@web/core/dialog/dialog";
// import { useService } from "@web/core/utils/hooks";
// import { markup } from "@odoo/owl";

// const { useRef, onMounted, onWillUnmount } = owl;

// // Webcam configuration service
// const useWebcamConfig = () => {
//     const getWebcamFlashFallbackModeConfig = async () => {
//         return await this.rpc("/web/dataset/call", {
//             model: "ir.config_parameter",
//             method: "get_webcam_flash_fallback_mode_config",
//         });
//     };

//     const setWebcamParams = async () => {
//         const forceFlash = (await getWebcamFlashFallbackModeConfig()) === "1";
        
//         Webcam.set({
//             width: 320,
//             height: 240,
//             dest_width: 320,
//             dest_height: 240,
//             image_format: "jpeg",
//             jpeg_quality: 90,
//             force_flash: forceFlash,
//             fps: 45,
//             swfURL: "/web_widget_image_webcam/static/src/lib/webcam.swf",
//         });
//     };

//     return {
//         setWebcamParams,
//     };
// };

// // Webcam Dialog Component
// class WebcamDialog extends Dialog {
//     setup() {
//         super.setup();
//         this.webcamConfig = useWebcamConfig();
//         this.webcamContainerRef = useRef("webcamContainer");
//         this.resultContainerRef = useRef("resultContainer");
//         this.imgData = null;
        
//         onMounted(async () => {
//             await this.initializeWebcam();
//         });
        
//         onWillUnmount(() => {
//             this.destroyWebcam();
//         });
//     }

//     async initializeWebcam() {
//         await this.webcamConfig.setWebcamParams();
//         Webcam.attach(this.webcamContainerRef.el);
        
//         // Disable save button initially
//         this.disableSaveButton();
        
//         // Set placeholder image
//         this.setPlaceholderImage();
//     }

//     destroyWebcam() {
//         Webcam.reset();
//     }

//     disableSaveButton() {
//         const saveButton = this.el.querySelector(".save_close_btn");
//         if (saveButton) {
//             saveButton.disabled = true;
//         }
//     }

//     enableSaveButton() {
//         const saveButton = this.el.querySelector(".save_close_btn");
//         if (saveButton) {
//             saveButton.disabled = false;
//         }
//     }

//     setPlaceholderImage() {
//         if (this.resultContainerRef.el) {
//             this.resultContainerRef.el.innerHTML = 
//                 '<img src="/web_widget_image_webcam/static/src/img/webcam_placeholder.png" alt="Webcam placeholder"/>';
//         }
//     }

//     takeSnapshot() {
//         Webcam.snap((data) => {
//             this.imgData = data;
//             // Display snapshot
//             if (this.resultContainerRef.el) {
//                 this.resultContainerRef.el.innerHTML = `<img src="${this.imgData}" alt="Webcam snapshot"/>`;
//             }
            
//             if (Webcam.live) {
//                 this.enableSaveButton();
//             }
//         });
//     }

//     saveAndClose() {
//         if (!this.imgData) return;

//         const imgDataBase64 = this.imgData.split(",")[1];
//         const approxImgSize = 3 * (imgDataBase64.length / 4) - 
//                             (imgDataBase64.match(/[=]+$/g) || []).length;

//         this.props.saveImage({
//             size: approxImgSize,
//             name: "web-cam-preview.jpeg",
//             type: "image/jpeg",
//             data: imgDataBase64,
//         });
        
//         this.props.close();
//     }
// }

// WebcamDialog.template = "web_widget_image_webcam.WebcamDialog";
// WebcamDialog.components = { Dialog };

// // Patch the ImageField to add webcam functionality
// patch(ImageField.prototype, "web_widget_image_webcam", {
//     setup() {
//         this._super();
//         this.dialog = useService("dialog");
//     },

//     onWebcamClicked() {
//         this.dialog.add(WebcamDialog, {
//             title: _t("WebCam Booth"),
//             saveImage: this.onFileUploaded.bind(this),
//         });
//     },
// });