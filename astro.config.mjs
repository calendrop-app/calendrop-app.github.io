// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import { satteri } from "@astrojs/markdown-satteri";

const site = "https://calendrop-app.github.io";

export default defineConfig({
  site,
  markdown: {
    processor: satteri(),
  },
  integrations: [
    starlight({
      title: "Calendrop",
      description: "A macOS menu bar app that covers every screen before your next Google Calendar meeting.",
      logo: {
        light: "./public/logo/calendrop-icon.svg",
        dark: "./public/logo/calendrop-icon-dark.svg",
        alt: "",
      },
      favicon: "/favicon.svg",
      head: [
        { tag: "link", attrs: { rel: "apple-touch-icon", href: "/apple-touch-icon.png" } },
        { tag: "meta", attrs: { property: "og:image", content: `${site}/logo/calendrop-icon-512.png` } },
        { tag: "meta", attrs: { name: "twitter:card", content: "summary" } },
      ],
      social: [{ icon: "github", label: "GitHub", href: "https://github.com/calendrop-app/Calendrop" }],
      editLink: {
        baseUrl: "https://github.com/calendrop-app/calendrop-app.github.io/edit/main/",
      },
      customCss: ["./src/styles/fonts.css", "./src/styles/starlight.css"],
      sidebar: [
        {
          label: "Start here",
          items: [
            { label: "Introduction", slug: "docs" },
            { label: "Install", slug: "docs/install" },
            { label: "Getting started", slug: "docs/getting-started" },
          ],
        },
        {
          label: "Using Calendrop",
          items: [
            { label: "The cut-in", slug: "docs/cut-in" },
            { label: "Settings", slug: "docs/settings" },
          ],
        },
        {
          label: "More",
          items: [
            { label: "Troubleshooting", slug: "docs/troubleshooting" },
            { label: "Release history", link: "/docs/releases/" },
          ],
        },
        {
          label: "Legal",
          items: [
            { label: "Privacy Policy", slug: "privacy" },
            { label: "Terms of Service", slug: "terms" },
          ],
        },
      ],
    }),
  ],
});
