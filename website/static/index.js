function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId })
    }).then((_res) => {
        // refresh the home page after deletion to see latest notes
        window.location.href = "/";
    }).catch((err) => {
        console.log("error in deleting note:", err);
    })
}