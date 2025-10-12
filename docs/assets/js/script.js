/**
 * jflatdb Documentation JavaScript
 * Handles navigation, mobile menu, and scroll behaviors
 */

(function () {
  "use strict";

  // ===== DOM Elements =====
  const sidebar = document.getElementById("sidebar");
  const sidebarToggle = document.getElementById("sidebarToggle");
  const navLinks = document.querySelectorAll(".nav-link");
  const sections = document.querySelectorAll(".section");
  const themeToggle = document.querySelector(".theme-toggle");

  if (themeToggle) {
    const savedTheme = localStorage.getItem("theme");
    const isDark = savedTheme === "dark";
    document.body.classList.toggle("dark-mode", isDark);
    themeToggle.textContent = isDark ? "☀️" : "🌙";

    themeToggle.addEventListener("click", () => {
      const dark = document.body.classList.toggle("dark-mode");
      themeToggle.textContent = dark ? "☀️" : "🌙";
      localStorage.setItem("theme", dark ? "dark" : "light");
    });
  }

  // ===== Mobile Sidebar Toggle =====
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", function () {
      sidebar.classList.toggle("active");
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener("click", function (event) {
      const isClickInsideSidebar = sidebar.contains(event.target);
      const isClickOnToggle = sidebarToggle.contains(event.target);

      if (
        !isClickInsideSidebar &&
        !isClickOnToggle &&
        sidebar.classList.contains("active")
      ) {
        sidebar.classList.remove("active");
      }
    });
  }

  // ===== Active Navigation on Click =====
  navLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      // Remove active class from all links
      navLinks.forEach(function (navLink) {
        navLink.classList.remove("active");
      });

      // Add active class to clicked link
      this.classList.add("active");

      // Close mobile sidebar after clicking
      if (window.innerWidth <= 768) {
        sidebar.classList.remove("active");
      }
    });
  });

  // ===== Active Navigation on Scroll =====
  function updateActiveNavOnScroll() {
    let currentSection = "";
    const scrollPosition = window.scrollY + 100; // Offset for better UX

    sections.forEach(function (section) {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;

      if (
        scrollPosition >= sectionTop &&
        scrollPosition < sectionTop + sectionHeight
      ) {
        currentSection = section.getAttribute("id");
      }
    });

    // Update active nav link based on current section
    navLinks.forEach(function (link) {
      link.classList.remove("active");
      if (link.getAttribute("href") === "#" + currentSection) {
        link.classList.add("active");
      }
    });
  }

  // Throttle scroll event for performance
  let scrollTimeout;
  window.addEventListener("scroll", function () {
    if (scrollTimeout) {
      window.cancelAnimationFrame(scrollTimeout);
    }

    scrollTimeout = window.requestAnimationFrame(function () {
      updateActiveNavOnScroll();
    });
  });

  // ===== Smooth Scroll Enhancement =====
  // Some browsers might not support CSS scroll-behavior
  navLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      const href = this.getAttribute("href");

      // Only handle internal links
      if (href.startsWith("#")) {
        e.preventDefault();

        const targetId = href.substring(1);
        const targetSection = document.getElementById(targetId);

        if (targetSection) {
          const offsetTop = targetSection.offsetTop - 20; // 20px offset

          window.scrollTo({
            top: offsetTop,
            behavior: "smooth",
          });

          // Update URL with hash fragment
          history.pushState(null, null, href);
        }
      }
    });
  });

  // ===== Copy Code Block Functionality (Optional Enhancement) =====
  // Add copy buttons to code blocks
  const codeBlocks = document.querySelectorAll("pre code");

  codeBlocks.forEach(function (codeBlock) {
    const pre = codeBlock.parentElement;
    const button = document.createElement("button");
    button.className = "copy-button";
    button.textContent = "Copy";
    button.style.cssText = `
      position: absolute;
      top: 8px;
      right: 8px;
      padding: 4px 8px;
      font-size: 12px;
      background-color: #2563eb;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      opacity: 0;
      transition: opacity 0.2s;
    `;

    // Make pre position relative for absolute button
    pre.style.position = "relative";

    // Show button on hover
    pre.addEventListener("mouseenter", function () {
      button.style.opacity = "1";
    });

    pre.addEventListener("mouseleave", function () {
      button.style.opacity = "0";
    });

    // Copy functionality
    button.addEventListener("click", function () {
      const code = codeBlock.textContent;

      // Use Clipboard API if available
      if (navigator.clipboard) {
        navigator.clipboard
          .writeText(code)
          .then(function () {
            button.textContent = "Copied!";
            setTimeout(function () {
              button.textContent = "Copy";
            }, 2000);
          })
          .catch(function (err) {
            console.error("Failed to copy:", err);
          });
      } else {
        // Fallback for older browsers
        const textarea = document.createElement("textarea");
        textarea.value = code;
        textarea.style.position = "fixed";
        textarea.style.opacity = "0";
        document.body.appendChild(textarea);
        textarea.select();

        try {
          document.execCommand("copy");
          button.textContent = "Copied!";
          setTimeout(function () {
            button.textContent = "Copy";
          }, 2000);
        } catch (err) {
          console.error("Failed to copy:", err);
        }

        document.body.removeChild(textarea);
      }
    });

    pre.appendChild(button);
  });

  // ===== Initialize Active Section on Page Load =====
  updateActiveNavOnScroll();

  // ===== Handle Browser Back/Forward Navigation =====
  window.addEventListener("popstate", function () {
    updateActiveNavOnScroll();
  });

  // ===== Log Initialization (for debugging) =====
  console.log("jflatdb documentation initialized");
  console.log("Sidebar navigation: ready");
  console.log("Mobile menu: ready");
  console.log("Smooth scroll: enabled");
})();
