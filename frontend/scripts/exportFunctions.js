// frontend/scripts/exportFunctions.js

/**
 * Export the table data to PDF
 */
function exportPDF() {
  const element = document.querySelector(".data-table");

  console.log("Starting PDF export...");

  // Temporarily apply the PDF-specific class
  const rotatedElements = document.querySelectorAll(".rotate");
  rotatedElements.forEach((el) => {
    el.classList.add("rotate-pdf");
    el.classList.remove("rotate");
  });

  // Get the courseType from the URL parameters
  const urlParams = new URLSearchParams(window.location.search);
  const courseType = urlParams.get("courseType");

  // Replace hyphens with underscores and use it in the filename
  const courseTypeFormatted = courseType
    ? courseType.replace(/-/g, "_")
    : "Degree_Roadmap";

  console.log(courseTypeFormatted);
  const opt = {
    margin: 0.1,
    filename: `${courseTypeFormatted}_2024-2025.pdf`, // Dynamic filename
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: {
      scale: 2,
      logging: true,
    },
    jsPDF: {
      unit: "in",
      format: [16.5, 13.2],
      orientation: "landscape",
    },
  };
  console.log(opt);
  html2pdf()
    .from(element)
    .set(opt)
    .save()
    .then(() => {
      // Restore the original class after export
      rotatedElements.forEach((el) => {
        el.classList.add("rotate");
        el.classList.remove("rotate-pdf");
      });
      console.log("PDF export successful.");
    })
    .catch((error) => {
      console.error("Error exporting PDF:", error);
      // Restore the original class if an error occurs
      rotatedElements.forEach((el) => {
        el.classList.add("rotate");
        el.classList.remove("rotate-pdf");
      });
    });
}

/**
 * Export the table data to Excel
 */
// function exportExcel() {
//   const table = document.querySelector(".data-table");
//   const wb = XLSX.utils.table_to_book(table, { sheet: "Sheet JS" });
//   // Get the courseType from the URL parameters
//   const urlParams = new URLSearchParams(window.location.search);
//   const courseType = urlParams.get("courseType");

//   // Replace hyphens with underscores and use it in the filename
//   const courseTypeFormatted = courseType
//     ? courseType.replace(/-/g, "_")
//     : "Degree_Roadmap";
//   XLSX.writeFile(wb, `${courseTypeFormatted}_2024-2025.xlsx`);
// }

// export { exportPDF, exportExcel };
export { exportPDF };
