export const buildTicketFormData = (ticket) => {
  const formData = new FormData();

  formData.append("priority", ticket.priority);
  formData.append("subject", ticket.subject);

  if (ticket.description) {
    formData.append("description", ticket.description);
  }

  if (ticket.files && ticket.files.length > 0) {
    ticket.files.forEach((file) => {
      formData.append("files", file); 
    });
  }

  return formData;
};
