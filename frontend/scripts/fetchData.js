// frontend/scripts/fetchData.js

import { updateDepartmentTitle, renderCourseTable } from "./renderFunctions.js";
import { makeCellsEditable, addExportListeners } from "./eventHandlers.js";

// Function to get URL parameters
function getUrlParams() {
  const urlParams = new URLSearchParams(window.location.search);
  return {
    courseType: urlParams.get("courseType") || "bachelor-social-work-courses",
    course: urlParams.get("course") || "Default Course",
    degree: urlParams.get("degree") || "Default Degree",
    college: urlParams.get("college") || "Default College",
  };
}

// Fetch data from the backend
function fetchData() {
  const { courseType, course, degree, college } = getUrlParams();
  const apiUrl = `https://flask-dp-gmaqhzfdfcadgncp.centralus-01.azurewebsites.net/api/${courseType}`;

  // Update the dynamic content based on URL parameters
  document.getElementById("degreeName").innerText = degree;
  document.getElementById("departmentTitle").innerText = course;

  return fetch(apiUrl) // Return the fetch promise
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      console.log("Data fetched successfully:", data); // Log fetched data
      initializeApp(data); // Initialize the app with the fetched data
      return data; // Return the data for further processing
    })
    .catch((error) => {
      console.error("Error loading JSON data:", error); // Handle any errors
      return null; // Return null in case of error
    });
}

/**
 * Initialize the application
 * @param {Object} courseData - The course data from the backend
 */
function initializeApp(courseData) {
  const departmentData = courseData[0];
  updateDepartmentTitle(departmentData.department);
  renderCourseTable(departmentData);
  makeCellsEditable();
  addExportListeners();
}

// Call fetchData to start the process
fetchData();

export { fetchData, initializeApp };
