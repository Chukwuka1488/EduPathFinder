// frontend/scripts/updateDepartmentTitle.js

/**
 * Update the department title in the DOM
 * @param {string} department - The department name
 */
function updateDepartmentTitle(department) {
  const navDepartmentTitle = document.getElementById("departmentTitle"); // Title in the navbar
  const tableDepartmentTitle = document.getElementById("tableDepartmentTitle"); // Title in the table header

  if (navDepartmentTitle) {
    navDepartmentTitle.innerText = department; // Update the navbar title
  }

  if (tableDepartmentTitle) {
    tableDepartmentTitle.innerText = department; // Update the table title
  }
}

export { updateDepartmentTitle };
