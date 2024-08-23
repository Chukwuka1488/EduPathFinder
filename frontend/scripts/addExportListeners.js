// frontend/scripts/addExportListeners.js
// import { exportPDF, exportExcel } from "./exportFunctions.js";
// import { exportPDF } from "./exportFunctions.js";
// /**
//  * Add event listeners for export buttons
//  */
// function addExportListeners() {
//   //   document.getElementById("exportExcel").addEventListener("click", () => {
//   //     exportExcel();
//   //   });
//   document.getElementById("exportPDF").addEventListener("click", () => {
//     exportPDF();
//   });
// }

// export { addExportListeners };
import { exportPDF } from "./exportFunctions.js";

/**
 * Add event listeners for export buttons
 */
function addExportListeners() {
  const exportPDFButton = document.getElementById("exportPDF");

  // Ensure the listener is only added once
  exportPDFButton.addEventListener(
    "click",
    () => {
      exportPDF();
    },
    { once: true }
  );
}

export { addExportListeners };
