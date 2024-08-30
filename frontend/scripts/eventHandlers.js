// frontend/scripts/eventHandlers.js
import { makeCellsEditable } from "./makeCellsEditable.js";
import { addExportListeners } from "./addExportListeners.js";
// import { exportPDF, exportExcel } from "./exportFunctions.js";
// import { exportPDF, exportExcel } from "./exportFunctions.js";

// Initialize the editable cells
makeCellsEditable();

// Add event listeners for export buttons
addExportListeners();

// Export all functions from eventHandlers.js
// export { makeCellsEditable, addExportListeners, exportPDF, exportExcel };
export { makeCellsEditable, addExportListeners };
