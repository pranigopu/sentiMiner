# WORKING NOTES
## Anonymous functions in JavaScript
Functions in JavaScript can be anonymous.
```
function() {
  alert('unicorn!');
}
```
And if you put that whole anonymous function in parentheses and then add parentheses after it, it’s a self-executing function. Meaning it’s called the moment it’s defined.
```
(function() {
  alert('unicorn!');
})();
```
If your code is complicated and long it’s often simpler to just put it in another JS file and reference it like so:
```
(function () {
  var script = document.createElement('script');
  script.src = 'someRandomCode.js';
  document.body.appendChild(script);
})();
```

## Accessing the DOM automatically through JavaScript
Consider an HTML document that includes a script that contains code requiring access to certain elements of the DOM, or event handlers associated with events of certain elements of the DOM. Also consider that these event handlers require accessing elements from the DOM. To ensure proper interpretation of the JavaScript code _(JavaScript is interpreted, not compiled, which is what makes it an effective web development scripting language)_, we must make sure the DOM gets loaded before the script, so that the interpretation happens without errors _(for example, if the DOM is not loaded for the script and the script requires access to some element in the DOM, a NULL value is returned instead of the required element)_. To do this, we can simply include the script after the required elements present in the HTML document's body element.

### REFERENCES:
- https://stackoverflow.com/questions/26107125/cannot-read-property-addeventlistener-of-null

## Content Security Policy (CSP) for inline script
CSP by default prevents execution of inline script, due to the danger of script injection by unwanted third parties.

### REFERENCES:
- Why is inline script & style execution dangerous?<br>https://content-security-policy.com/unsafe-inline/