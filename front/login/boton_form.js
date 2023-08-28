const inputFields = document.querySelectorAll('.user-box input');
    inputFields.forEach(input => {
      input.addEventListener('input', () => {
        if (input.value) {
          input.classList.add('active');
        } else {
          input.classList.remove('active');
        }
      });
    });