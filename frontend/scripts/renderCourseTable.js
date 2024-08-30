// frontend/scripts/renderCourseTable.js
import {
  calculateYearRowSpan,
  calculateSemesterRowSpan,
  addBlankRows,
  appendYearRow,
  appendSemesterRows,
} from "./utilityFunctions.js";
import { addDegreeSummaryRows } from "./addDegreeSummaryRows.js";
import { addCoreGECInfo } from "./addCoreGECInfo.js";
import { generateCustomRow } from "./generateCustomRow.js";

/**
 * Render the course table with the provided data
 * @param {Object} data - The course data
 */
function renderCourseTable(data) {
  const tableBody = document.getElementById("courseTableBody");
  tableBody.innerHTML = ""; // Clear any existing content

  let rowIndex = 0; // Initialize row index to manage row insertion correctly

  data.years.forEach((year, index) => {
    const yearRowSpan = calculateYearRowSpan(year);
    appendYearRow(tableBody, year.year, yearRowSpan);
    rowIndex++; // Increment rowIndex after the year row

    year.semesters.forEach((semester) => {
      const semesterRowSpan = calculateSemesterRowSpan(semester);
      appendSemesterRows(tableBody, semester, semesterRowSpan);
      rowIndex += semesterRowSpan; // Increment rowIndex by the semester span
    });

    // Add custom row after the first year
    if (year.year === "First Year") {
      const customRow1 = document.createElement("tr");
      customRow1.className = "bg-gray-600";
      customRow1.innerHTML = generateCustomRow();
      tableBody.appendChild(customRow1);
    }

    // Add custom row after the second year
    if (year.year === "Second Year") {
      const customRow2 = document.createElement("tr");
      customRow2.className = "bg-custom-orange";
      //   TODO: Below Year Two
      customRow2.innerHTML = `
          <th colspan="10" class="text-white border-transparent">
            <h6 class="text-center font-semibold" style="font-size: 10px; margin: 0px;">
              <p>${data.belowYearTwo}</p>
              </h6>
          </th>
        `;
      tableBody.appendChild(customRow2);

      // Add blank rows and core GEC info
      addCoreGECInfo(tableBody);

      const customRow2After = document.createElement("tr");
      customRow2After.className = "bg-custom-orange";
      //   TODO: Above Year Three
      customRow2After.innerHTML = `
          <th colspan="10" class="text-white border-transparent">
            <h6 class="text-center font-semibold" style="font-size: 10px; margin: 0px;">
              <p>${data.aboveYearThree}</p>
              </h6>
          </th>
        `;
      tableBody.appendChild(customRow2After);

      const customRow1Again = document.createElement("tr");
      customRow1Again.className = "bg-gray-600";
      customRow1Again.innerHTML = generateCustomRow();
      tableBody.appendChild(customRow1Again);
    }

    // Add custom rows before and after the third year
    if (year.year === "Third Year") {
      const customRow3Before = document.createElement("tr");
      customRow3Before.className = "bg-custom-orange";
      //   TODO: Above Year Four
      customRow3Before.innerHTML = `
          <th colspan="10" class="text-white border-transparent">
            <h6 class="text-center font-semibold" style="font-size: 10px; margin: 0px;">
             <p>${data.aboveYearFour}</p>
             </h6>
          </th>
        `;
      tableBody.appendChild(customRow3Before);

      const customRow3After = document.createElement("tr");
      customRow3After.className = "bg-gray-600";
      customRow3After.innerHTML = generateCustomRow();
      tableBody.appendChild(customRow3After);
    }

    // Add custom rows before the fourth year
    if (year.year === "Fourth Year") {
      addDegreeSummaryRows(tableBody, data);
    }
  });
}

export { renderCourseTable };
