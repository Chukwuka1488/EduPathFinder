// frontend/scripts/updateCourseData.js
import { getCollectionName } from "./getCollectionName.js";

/**
 * Update course data on the backend
 * @param {HTMLElement} cell - The cell being edited
 * @param {string} newValue - The new value entered by the user
 */
function updateCourseData(cell, newValue) {
  console.log("Starting to update course data...");

  const row = cell.parentElement;
  console.log("Row data extracted:", row);

  // Identify the course title cell
  const courseTitleCell = row.querySelector("td[data-key='title']");
  console.log(`Course title cell: ${courseTitleCell}`);
  if (!courseTitleCell) {
    console.error("Could not find the course title cell.");
    return;
  }
  const courseTitle = courseTitleCell.innerText.trim();

  if (!courseTitle) {
    console.error("Invalid course title found:", courseTitle);
    return;
  }

  // Ensure the field being updated is correct
  const fieldToUpdate = cell.dataset.key; // Ensure each cell has a data-key attribute
  if (!fieldToUpdate) {
    console.error("Could not find the data-key attribute for the field.");
    return;
  }
  console.log(`Field to update: ${fieldToUpdate}`);
  console.log(
    `Updating course data for course title: ${courseTitle}, field: ${fieldToUpdate}, new value: ${newValue}`
  );

  // Get the correct collection name
  const collectionName = getCollectionName();
  console.log("Collection name identified:", collectionName);

  // Prepare the data to send to the backend
  const updateData = {
    collectionName: collectionName,
    courseTitle: courseTitle,
    field: fieldToUpdate,
    value: newValue,
  };

  console.log("Update data prepared:", updateData);

  fetch(
    `https://flask-dp-gmaqhzfdfcadgncp.centralus-01.azurewebsites.net/api/update-course`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData),
    }
  )
    .then((response) => {
      console.log("Response received from backend:", response);
      if (!response.ok) {
        throw new Error("Failed to update course data");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Update successful, data returned from backend:", data);
    })
    .catch((error) => console.error("Error updating course data:", error));
}

export { updateCourseData };
