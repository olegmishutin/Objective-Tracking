document.getElementById('participant_page_button').onclick = () => {
    document.getElementById('participant_page').style.display = 'flex'
    document.getElementById('participant_tasks').style.display = 'none'
}

document.getElementById('task_page_button').onclick = () => {
    document.getElementById('participant_tasks').style.display = 'flex'
    document.getElementById('participant_page').style.display = 'none'
}