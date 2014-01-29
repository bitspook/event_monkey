---
title: "{{title}}"
layout: post
categories: ['greetings','sms','message','quotes','fb-status']
date: {{date}}
comments: false
images: ["{{images[0]}}","{{images[1]}}"]
excerpt: "{{excerpt}}"
keywords: [{% for keyword in keywords %} "{{keyword}}", {% endfor %}]
description: "{{title}} {{keyword}}"
tags: [{% for tag in tags %} "{{tag}}", {% endfor %}]

---

<h1 style="font-size: 14px">
<strong>best {{keyword}}</strong>
</h1>

> {{messages[0]}}

<h2 style="font-size: 18px">
<strong>best {{keyword}}</strong>
</h2>

<!-- ![{{title}}]({{image1}}) -->

> **{{messages[1]}}**

<h2 style="font-size: 18px">
{{title}}
</h2>

> {{messages[2]}}

###You may also like
{% raw %}
{% for p in site.related_posts %}
[**{{p.title}}**]({{p.url}})
{% endfor %}
{% endraw %}

####Incoming search terms
{% for search_term in search_terms %}[**{{search_term}}**]{% raw %}({{page.url}}){% endraw %}{% endfor %}

