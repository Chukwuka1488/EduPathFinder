// frontend/scripts/utilityFunctions.js

/**
 * Calculate the row span needed for a year
 * @param {Object} year - The year data
 * @returns {number} - The calculated row span for the year
 */
function calculateYearRowSpan(year) {
  const rowSpan =
    year.semesters.reduce((acc, semester) => acc + semester.courses.length, 1) +
    year.semesters.length;
  return rowSpan;
}

/**
 * Calculate the row span needed for a semester
 * @param {Object} semester - The semester data
 * @returns {number} - The calculated row span for the semester
 */
function calculateSemesterRowSpan(semester) {
  const rowSpan = semester.courses.length + 1; // +1 for the total hours row
  return rowSpan;
}

/**
 * Add a specified number of blank rows to the table
 * @param {HTMLElement} tableBody - The table body element
 * @param {number} numRows - The number of blank rows to add
 */
function addBlankRows(tableBody, numRows) {
  for (let i = 0; i < numRows; i++) {
    const blankRow = document.createElement("tr");
    const blankCell = document.createElement("td");
    blankCell.colSpan = 10; // Adjust colSpan to match the table structure
    blankCell.className = "border p-2 bg-gray-100"; // Optional: Add styles for blank rows
    blankRow.appendChild(blankCell);
    tableBody.appendChild(blankRow);
  }
}

/**
 * Append a row for the year with the correct row span
 * @param {HTMLElement} tableBody - The table body element
 * @param {string} year - The year
 * @param {number} rowSpan - The row span for the year
 */
function appendYearRow(tableBody, year, rowSpan) {
  const yearRow = document.createElement("tr");
  const yearCell = document.createElement("td");
  yearCell.className = "border p-2 text-center bg-custom-orange";
  yearCell.rowSpan = rowSpan;
  // Create a span element to rotate the text only
  const yearText = document.createElement("span");
  yearText.className = "rotate text-white"; // Apply rotation to the text only
  yearText.textContent = year;

  yearCell.appendChild(yearText);
  yearRow.appendChild(yearCell);
  tableBody.appendChild(yearRow);
}

/**
 * Append rows for a semester and its courses
 * @param {HTMLElement} tableBody - The table body element
 * @param {Object} semester - The semester data
 * @param {number} rowIndex - The starting row index
 */
function appendSemesterRows(tableBody, semester, rowIndex) {
  const semesterCell = createSemesterCell(semester);
  let firstRow = true;

  semester.courses.forEach((course) => {
    const row = document.createElement("tr");

    if (firstRow) {
      row.appendChild(semesterCell);
      firstRow = false;
    }

    appendCourseCells(row, course);
    tableBody.appendChild(row);
    rowIndex++;
  });

  appendTotalHoursRow(tableBody, semester);
}

/**
 * Create a cell for the semester with the correct row span
 * @param {Object} semester - The semester data
 * @returns {HTMLElement} - The created semester cell
 */
function createSemesterCell(semester) {
  const semesterCell = document.createElement("td");
  semesterCell.className = "border p-2 text-center";
  semesterCell.rowSpan = calculateSemesterRowSpan(semester);
  // Create a span element to rotate the text only
  const semesterText = document.createElement("span");
  semesterText.className = "rotate text-white"; // Apply rotation to the text only
  semesterText.textContent = semester.semester;

  if (semester.semester.toLowerCase().includes("fall")) {
    semesterCell.classList.add("bg-custom-green");
  } else if (semester.semester.toLowerCase().includes("spring")) {
    semesterCell.classList.add("bg-custom-blue");
  } else {
    semesterCell.classList.add("bg-gray-500"); // Default color
  }

  semesterCell.appendChild(semesterText);
  return semesterCell;
}

/**
 * Append cells for a course's data
 * @param {HTMLElement} row - The row to append cells to
 * @param {Object} course - The course data
 */
function appendCourseCells(row, course) {
  // Define the order of the keys as they should appear in the table
  const keysOrder = [
    { key: "important", displayName: "Important" },
    { key: "hours", displayName: "Hours" },
    { key: "courseNumber", displayName: "Course #" },
    { key: "title", displayName: "Course Title" },
    { key: "minGrade", displayName: "Min. Grade" },
    { key: "gec", displayName: "GEC" },
    { key: "prerequisite", displayName: "Prerequisite" },
    { key: "notes", displayName: "Additional Notes" },
  ];

  keysOrder.forEach(({ key }) => {
    const cell = document.createElement("td");
    cell.className = "border p-2";
    cell.textContent = course[key] || ""; // Use an empty string if the course object doesn't have this key
    cell.setAttribute("data-key", key); // Add the data-key attribute for the cell
    row.appendChild(cell);
  });
}

/**
 * Append a row for the total hours of a semester
 * @param {HTMLElement} tableBody - The table body element
 * @param {Object} semester - The semester data
 * @param {number} rowIndex - The starting row index
 */
function appendTotalHoursRow(tableBody, semester, rowIndex) {
  const totalRow = document.createElement("tr");
  const totalCell = document.createElement("td");

  totalCell.className = "border p-2 text-left font-bold bg-gray-300";
  totalCell.colSpan = 8; // Adjust colSpan to match the table structure
  totalCell.textContent = `${semester.totalSemesterHours} Semester Total Hours`; // Use totalSemesterHours from data
  totalRow.appendChild(totalCell);
  tableBody.appendChild(totalRow);
}

export {
  calculateYearRowSpan,
  calculateSemesterRowSpan,
  addBlankRows,
  appendYearRow,
  appendSemesterRows,
  createSemesterCell,
  appendCourseCells,
  appendTotalHoursRow,
};
