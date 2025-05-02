// Show MFA when password has input
if(document.getElementById('password')){
    document.getElementById('password').addEventListener('input', (e) => {
        const mfaSection = document.getElementById('mfa-section');
        mfaSection.style.display = e.target.value.length >= 8 ? 'block' : 'none';
    });
}

// Biometric Mock
if(document.getElementById('biometric-btn')) {
    document.getElementById('biometric-btn').addEventListener('click', () => {
        alert("Biometric authentication would trigger here in production (WebAuthn API)");
    });
}

// Change password
document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility
    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
            }
        });
    });
    
    // Password strength checker
    const newPassword = document.getElementById('newPassword');
    const strengthBar = document.querySelector('.password-strength .progress-bar');
    const criteria = {
        length: document.getElementById('length'),
        number: document.getElementById('number'),
        special: document.getElementById('special')
    };
    
    newPassword.addEventListener('input', function() {
        const password = this.value;
        let strength = 0;
        
        // Length check
        if (password.length >= 8) {
            strength += 30;
            criteria.length.classList.add('valid');
            criteria.length.classList.remove('text-muted');
        } else {
            criteria.length.classList.remove('valid');
            criteria.length.classList.add('text-muted');
        }
        
        // Number check
        if (/\d/.test(password)) {
            strength += 30;
            criteria.number.classList.add('valid');
            criteria.number.classList.remove('text-muted');
        } else {
            criteria.number.classList.remove('valid');
            criteria.number.classList.add('text-muted');
        }
        
        // Special char check
        if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
            strength += 40;
            criteria.special.classList.add('valid');
            criteria.special.classList.remove('text-muted');
        } else {
            criteria.special.classList.remove('valid');
            criteria.special.classList.add('text-muted');
        }
        
        // Update strength bar
        strengthBar.style.width = strength + '%';
        
        if (strength < 50) {
            strengthBar.className = 'progress-bar bg-danger';
        } else if (strength < 80) {
            strengthBar.className = 'progress-bar bg-warning';
        } else {
            strengthBar.className = 'progress-bar bg-success';
        }
        
        // Check password match
        const confirmPassword = document.getElementById('confirmPassword');
        if (confirmPassword.value && password !== confirmPassword.value) {
            confirmPassword.classList.add('is-invalid');
        } else {
            confirmPassword.classList.remove('is-invalid');
        }
    });
    
    // Confirm password check
    document.getElementById('confirmPassword').addEventListener('input', function() {
        if (this.value !== newPassword.value) {
            this.classList.add('is-invalid');
        } else {
            this.classList.remove('is-invalid');
        }
    });
    
    // Form submission
    document.getElementById('changePasswordForm').addEventListener('submit', function(e) {
        e.preventDefault();
        // Add your password change logic here
        alert('Password changed successfully!');
    });
});

// OTP
document.addEventListener('DOMContentLoaded', function() {
    // OTP input auto-focus and navigation
    const otpInputs = document.querySelectorAll('.otp-input');
    
    otpInputs.forEach((input, index) => {
        // Auto-tab to next input when a digit is entered
        input.addEventListener('input', function() {
            if (this.value.length === 1) {
                if (index < otpInputs.length - 1) {
                    otpInputs[index + 1].focus();
                }
            }
        });
        
        // Handle backspace
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Backspace' && this.value.length === 0) {
                if (index > 0) {
                    otpInputs[index - 1].focus();
                }
            }
        });
    });
    
    // Combine OTP digits before submission
    document.getElementById('otpVerificationForm').addEventListener('submit', function(e) {
        let fullOtp = '';
        otpInputs.forEach(input => {
            fullOtp += input.value;
        });
        document.getElementById('fullOtp').value = fullOtp;
    });
    
    // Countdown timer
    let timeLeft = 179; // 2 minutes 59 seconds
    const timer = document.getElementById('timer');
    
    const countdown = setInterval(() => {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        if (timeLeft <= 0) {
            clearInterval(countdown);
            timer.textContent = "Expired";
            timer.classList.add('text-danger');
        } else {
            timeLeft--;
        }
    }, 1000);
    
    // Resend OTP functionality
    document.querySelector('.resend-link').addEventListener('click', function() {
        alert('New verification code sent!');
        timeLeft = 179; // Reset timer
        timer.textContent = "02:59";
        timer.classList.remove('text-danger');
    });
});

// Upload File
document.addEventListener('DOMContentLoaded', function() {
    // File upload handling
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('documentUpload');
    const previewSection = document.getElementById('previewSection');
    const filePreview = document.getElementById('filePreview');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const removeFile = document.getElementById('removeFile');
    
    // Click on dropzone triggers file input
    dropzone.addEventListener('click', () => fileInput.click());
    
    // Handle file selection
    fileInput.addEventListener('change', function(e) {
        if (this.files.length > 0) {
            const file = this.files[0];
            showPreview(file);
        }
    });
    
    // Drag and drop handling
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.style.borderColor = '#2a5bd7';
        dropzone.style.backgroundColor = '#e8f0fe';
    });
    
    dropzone.addEventListener('dragleave', () => {
        dropzone.style.borderColor = '#dee2e6';
        dropzone.style.backgroundColor = '#f8f9fa';
    });
    
    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.style.borderColor = '#dee2e6';
        dropzone.style.backgroundColor = '#f8f9fa';
        
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            showPreview(e.dataTransfer.files[0]);
        }
    });
    
    // Remove file
    removeFile.addEventListener('click', function() {
        fileInput.value = '';
        previewSection.classList.add('d-none');
        dropzone.style.display = 'block';
    });
    
    // Show file preview
    function showPreview(file) {
        // Basic validation
        const validTypes = ['application/pdf', 'image/jpeg', 'image/png', 
                          'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                          'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
        
        if (!validTypes.includes(file.type)) {
            alert('Please upload a valid file type (PDF, Word, Excel, JPG, PNG)');
            return;
        }
        
        if (file.size > 25 * 1024 * 1024) {
            alert('File size exceeds 25MB limit');
            return;
        }
        
        // Update UI
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        
        // Show preview if image
        if (file.type.includes('image')) {
            const reader = new FileReader();
            reader.onload = (e) => filePreview.src = e.target.result;
            reader.readAsDataURL(file);
            filePreview.style.display = 'block';
        } else {
            filePreview.style.display = 'none';
        }
        
        previewSection.classList.remove('d-none');
        dropzone.style.display = 'none';
        
        // Auto-fill document name if empty
        if (!document.getElementById('docName').value) {
            document.getElementById('docName').value = file.name.split('.')[0];
        }
    }
    
    // Toggle expiry date field
    document.getElementById('setExpiry').addEventListener('change', function() {
        document.getElementById('expiryDateGroup').style.display = 
            this.checked ? 'block' : 'none';
    });
    
    // Format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }
});

//  File status/action
document.addEventListener('DOMContentLoaded', function() {
    // Handle digital signature submission
    document.querySelector('.btn-sign').addEventListener('click', function() {
        // Save optional description
        const description = document.getElementById('documentDescription').value;
        console.log('Description saved:', description);
        
        // Trigger digital signature flow
        if (confirm('Apply your digital signature to this document?')) {
            alert('Document signed successfully!');
            window.location.href = "{% url 'document_list' %}";
        }
    });
    
    // Handle report submission
    document.getElementById('reportForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Problem report submitted. Our team will contact you shortly.');
        const modal = bootstrap.Modal.getInstance(document.getElementById('reportModal'));
        modal.hide();
    });
});