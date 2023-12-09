
  document.addEventListener('DOMContentLoaded', function() {
    console.log('Document loaded');
  
    var readMoreLinks = document.querySelectorAll('.read-more-link');
  
    readMoreLinks.forEach(function(link) {
      link.addEventListener('click', function(event) {
        event.preventDefault();
        console.log('Read more link clicked');
  
        var productDescription = this.parentNode.querySelector('.full_description');
        var shortDescription = this.parentNode.querySelector('.short_description');
  
        if (productDescription && shortDescription) {
          productDescription.style.display = 'block';
          shortDescription.style.display = 'none';
          this.style.display = 'none';
        }
      });
    });
  });
  
    