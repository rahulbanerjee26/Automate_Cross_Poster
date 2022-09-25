from devto import DevtoPoster
from wp import WordpressPoster
from medium import MediumPoster
from hashnode import HashnodePoster
import os
from dotenv import load_dotenv
from utils import createGists, markDownToHtml,getCodeSnippetsFromMarkdown, replaceCodeSnippetsWithGists

load_dotenv()

WP_USERNAME = os.environ.get("WP_USERNAME")
WP_PASSWORD = os.environ.get("WP_PASSWORD")
MEDIUM_TOKEN = os.environ.get("MEDIUM_TOKEN")
DEVTO_TOKEN = os.environ.get("DEVTO_TOKEN")
HASNODE_TOKEN = os.environ.get("HASHNODE_TOKEN")
HASHNODE_PUBLICATION_ID = os.environ.get("HASHNODE_PUBLICATION_ID")
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

domain ="Your Domain"
tags = ["python", "linearprogramming", "tutorial", "datascience"]
title = "My First Posting Using the API"
post_content_html = None
post_content_md = None
wp_post_url = None
feature_image_url = ""

post_wp = True
post_medium = True
post_devto = True
post_hashnode = True


with open("index.md", "r") as f:
    post_content_md = f.read()
    

snippets = getCodeSnippetsFromMarkdown(post_content_md)

gistURLs = createGists(
    GITHUB_TOKEN,
    snippets,
    public=True
)

new_content = replaceCodeSnippetsWithGists(
    post_content_md,
    gistURLs,
    title,
    hashnode=post_hashnode,
    devto=post_devto,
    medium=post_medium,
    wp=post_wp
)

# ---------------- Wordpress -------------------------------------
if post_wp:
    try:
        wp_post_content_html = markDownToHtml(new_content['wp'])
        wp = WordpressPoster(domain, WP_USERNAME, WP_PASSWORD)
        featuredImageID = wp.upload_media('./CrossPostCover.png',alt_text="Cover Image")
        categoryIDs = wp.get_category_ids(["tutorial"])
        tagIDs = wp.get_tag_ids(tags)
        wp_response = wp.create_post_wordpress(
            title, wp_post_content_html, "draft", categoryIDs, tagIDs, featuredImageID
        )
        wp_post_url = wp_response.get("guid").get("raw")
        feature_image_url = wp_response.get("jetpack_featured_media_url")
        print(f"Find WordPress Post: {wp_post_url}")
    except:
        print("Error when posting to WP")


# ------------------ Medium -------------------------------------
if post_medium:
    medium_post_content_html = markDownToHtml(new_content['medium'])
    try:
        medium = MediumPoster(MEDIUM_TOKEN, domain)
        medium_url = medium.create_post_medium(
            title, medium_post_content_html, canonicalUrl=wp_post_url, tags=tags
        )
        print(f'Find Medium Post: {medium_url}')
    except:
        print("Error when posting to Medium")


# -------------------- Dev.to -------------------------------------
if post_devto:
    try:
        devto = DevtoPoster(DEVTO_TOKEN, domain)
        devto_url = devto.create_post_devto(
            title,
            new_content['devto'],
            tags=tags,
            canonical_url=wp_post_url,
            main_image=feature_image_url,
        )
        print(f"Find Dev.to Post: {devto_url}")
    except:
        print("Error when posting to Devto")

# -------------------- Hashnode -------------------------------------
if post_hashnode:
    try:
        hasnode = HashnodePoster(
            HASNODE_TOKEN, "YOUR HASHNODE BLOG"
        )
        hashnode_url = hasnode.create_post_hashnode(
            title,
            new_content['hashnode'],
            HASHNODE_PUBLICATION_ID,
            tags,
            canonicalUrl=wp_post_url,
        )
        print(f"Find Hashnode Post: {hashnode_url}")
    except:
        print("Error when posting to Hahsnode")


