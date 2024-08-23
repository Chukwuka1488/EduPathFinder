// frontend/scripts/getCollectionName.js

/**
 * Get the correct collection name
 * @returns {string} The collection name
 */
function getCollectionName() {
  // Get the courseType from the URL parameters
  const urlParams = new URLSearchParams(window.location.search);
  const courseType = urlParams.get("courseType");

  // Replace hyphens with underscores to form the collection name
  if (courseType) {
    return courseType.replace(/-/g, "_");
  } else {
    console.error("Course type not found in the URL.");
    return null;
  }
}

export { getCollectionName };
