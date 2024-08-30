// frontend/scripts/main.js

let currentPage = 1;
const limit = 20;
let currentType = "undergraduate"; // Default degree type

// Fetch and render initial data
fetchDegrees(currentType, currentPage);

// Add event listeners to buttons
document.getElementById("undergraduateBtn").addEventListener("click", () => {
  currentType = "undergraduate";
  currentPage = 1; // Reset to the first page
  fetchDegrees(currentType, currentPage);
});

document.getElementById("graduateBtn").addEventListener("click", () => {
  currentType = "graduate";
  currentPage = 1; // Reset to the first page
  fetchDegrees(currentType, currentPage);
});

/**
 * Fetches and renders degrees based on the current type and page.
 * @param {string} type - The degree type (e.g., "undergraduate", "graduate").
 * @param {number} page - The page number for pagination.
 */
// function fetchDegrees(type, page) {
//   console.log(`Fetching degrees for type: ${type}, page: ${page}`); // Debugging statement
//   fetch(
//     "https://flask-dp-gmaqhzfdfcadgncp.centralus-01.azurewebsites.net/api/colleges-degrees",
//     { cache: "no-store" } // This line disables caching for this request
//   )
//     .then((response) => {
//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }
//       return response.json(); // Ensure the response is JSON
//     })
//     .then((data) => {
//       console.log("Data received:", data);

//       if (!Array.isArray(data)) {
//         throw new Error("Expected an array of degrees");
//       }

//       const filteredData = filterByType(data, type);
//       const totalPages = Math.ceil(filteredData.length / limit);

//       const paginatedData = paginateData(filteredData, page, limit);

//       console.log("Rendering degrees to the HTML...");
//       renderDegrees(paginatedData);
//       renderPagination(totalPages, page);

//       console.log(`Total pages: ${totalPages}, Current page: ${page}`); // Debugging statement
//     })
//     .catch((error) => console.error("Error fetching degrees:", error));
// }

function fetchDegrees(type, page) {
  console.log(`Fetching degrees for type: ${type}, page: ${page}`); // Debugging statement
  fetch(
    // "https://flask-dp-gmaqhzfdfcadgncp.centralus-01.azurewebsites.net/api/colleges-degrees",
    "http://127.0.0.1:5001/api/colleges-degrees",
    { cache: "no-store" } // This line disables caching for this request
  )
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json(); // Ensure the response is JSON
    })
    .then((data) => {
      console.log("Data received:", data);

      if (!Array.isArray(data)) {
        throw new Error("Expected an array of degrees");
      }

      const filteredData = filterByType(data, type);

      // Sort the filtered data alphabetically by the course name
      const sortedData = filteredData.sort((a, b) =>
        a.course.localeCompare(b.course)
      );

      const totalPages = Math.ceil(sortedData.length / limit);

      const paginatedData = paginateData(sortedData, page, limit);

      console.log("Rendering degrees to the HTML...");
      renderDegrees(paginatedData);
      renderPagination(totalPages, page);

      console.log(`Total pages: ${totalPages}, Current page: ${page}`); // Debugging statement
    })
    .catch((error) => console.error("Error fetching degrees:", error));
}

/**
 * Filters degrees by type (e.g., undergraduate, graduate).
 * @param {Array} degrees - Array of degree objects.
 * @param {string} type - Type to filter by.
 * @returns {Array} - Filtered degrees.
 */
function filterByType(degrees, type) {
  console.log(`Filtering degrees for type: ${type}`); // Debugging statement

  return degrees.filter((degree) => {
    if (type === "undergraduate") {
      return degree.degree.toLowerCase().includes("bachelor");
    } else if (type === "graduate") {
      return degree.degree.toLowerCase().includes("master");
    }
    return false;
  });
}

function paginateData(data, page, limit) {
  const startIndex = (page - 1) * limit;
  const endIndex = page * limit;
  return data.slice(startIndex, endIndex);
}

function renderDegrees(degrees) {
  const container = document.getElementById("degree-cards");
  container.innerHTML = ""; // Clear existing content

  degrees.forEach((degree) => {
    const card = document.createElement("div");
    card.className =
      "max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow bg-gray-200 dark:bg-gray-800 dark:border-gray-700";
    card.innerHTML = `
      <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">${degree.course}</h5>
      <p class="text-lg font-semibold text-gray-700 dark:text-gray-300">${degree.degree}</p>
      <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">${degree.college}</p>
      <a href="#" class="fetch-course-btn inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" data-course-type="${degree.courseType}" data-course="${degree.course}" data-degree="${degree.degree}" data-college="${degree.college}">
        Check RoadMap
        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9" />
        </svg>
      </a>
    `;
    container.appendChild(card);
  });

  // Add event listeners to the buttons
  const buttons = document.querySelectorAll(".fetch-course-btn");
  buttons.forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent the default link behavior
      const courseType = button.getAttribute("data-course-type");
      const course = button.getAttribute("data-course");
      const degreeName = button.getAttribute("data-degree");
      const college = button.getAttribute("data-college");
      const url = `roadmap.html?course=${encodeURIComponent(
        course
      )}&degree=${encodeURIComponent(degreeName)}&college=${encodeURIComponent(
        college
      )}&courseType=${courseType}`;
      window.location.href = url; // Redirect to the new URL
    });
  });

  console.log("Finished rendering all degrees."); // Final log after rendering
}

function renderPagination(totalPages, currentPage) {
  const paginationControls = document.getElementById("pagination-controls");
  paginationControls.innerHTML = ""; // Clear existing pagination controls

  console.log(`Rendering pagination for page ${currentPage} of ${totalPages}`); // Debugging statement

  if (currentPage > 1) {
    const prevButton = document.createElement("button");
    prevButton.className =
      "px-4 py-2 mx-1 bg-gray-300 text-gray-700 rounded hover:bg-gray-400";
    prevButton.textContent = "Previous";
    prevButton.onclick = () => {
      currentPage--;
      fetchDegrees(currentType, currentPage);
    };
    paginationControls.appendChild(prevButton);
  }

  for (let i = 1; i <= totalPages; i++) {
    const pageButton = document.createElement("button");
    pageButton.className = `px-4 py-2 mx-1 ${
      i === currentPage ? "bg-blue-600 text-white" : "bg-gray-300 text-gray-700"
    } rounded hover:bg-gray-400`;
    pageButton.textContent = i;
    pageButton.onclick = () => {
      currentPage = i;
      fetchDegrees(currentType, currentPage);
    };
    paginationControls.appendChild(pageButton);
  }

  if (currentPage < totalPages) {
    const nextButton = document.createElement("button");
    nextButton.className =
      "px-4 py-2 mx-1 bg-gray-300 text-gray-700 rounded hover:bg-gray-400";
    nextButton.textContent = "Next";
    nextButton.onclick = () => {
      currentPage++;
      fetchDegrees(currentType, currentPage);
    };
    paginationControls.appendChild(nextButton);
  }
}
