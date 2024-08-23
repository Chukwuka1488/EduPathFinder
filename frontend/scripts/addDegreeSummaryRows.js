// frontend/scripts/addDegreeSummaryRows.js

/**
 * Append rows for total degree hours and advanced minimum credit hours at the end of the 4th year
 * @param {HTMLElement} tableBody - The table body element
 * @param {Object} data - The entire data object for the department
 */
function addDegreeSummaryRows(tableBody, data) {
  // Row for Total Degree Hours
  const totalDegreeRow = document.createElement("tr");
  const totalDegreeCell = document.createElement("td");
  totalDegreeCell.className = "text-left";
  totalDegreeCell.colSpan = 8; // Adjust colSpan for alignment
  totalDegreeCell.textContent = `${data.totalDegreeHours} TOTAL HOURS`;
  totalDegreeRow.appendChild(totalDegreeCell);

  // Adding approved date next to the Total Degree Hours
  const approvedCell = document.createElement("td");
  approvedCell.className = "text-right";
  approvedCell.colSpan = 2; // Adjust colSpan for alignment
  approvedCell.textContent = data.approved;
  totalDegreeRow.appendChild(approvedCell);

  tableBody.appendChild(totalDegreeRow);

  // Row for Advanced Minimum Credit Hours
  const advancedCreditsRow = document.createElement("tr");
  const advancedCreditsCell = document.createElement("td");
  advancedCreditsCell.className = "text-left";
  advancedCreditsCell.colSpan = 8; // Adjust colSpan for alignment
  advancedCreditsCell.textContent = `(${data.advancedMinimumCreditHours}) Advanced minimum credit hours`;
  advancedCreditsRow.appendChild(advancedCreditsCell);

  // Adding revised date next to the Advanced Minimum Credit Hours
  const revisedCell = document.createElement("td");
  revisedCell.className = "text-right";
  revisedCell.colSpan = 2; // Adjust colSpan for alignment
  revisedCell.textContent = data.revised;
  advancedCreditsRow.appendChild(revisedCell);

  tableBody.appendChild(advancedCreditsRow);
}

export { addDegreeSummaryRows };
