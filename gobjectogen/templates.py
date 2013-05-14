#
# gobjectogen - GObject generator
#
# Copyright (c) 2013 Eric Le Bihan <eric.le.bihan.dev@free.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

TEMPLATE_CLASS_HEADER = """
#ifndef {{header_guard}}
#define {{header_guard}}

#include <glib-object.h>

G_BEGIN_DECLS

#define {{ns_upper}}_TYPE_{{object_upper}} {{class_lower}}_get_type()

#define {{ns_upper}}_{{object_upper}}(obj) \\
	(G_TYPE_CHECK_INSTANCE_CAST((obj), \\
	{{ns_upper}}_TYPE_{{object_upper}}, {{class_camel}}))

#define {{ns_upper}}_{{object_upper}}_CLASS(klass) \\
	(G_TYPE_CHECK_CLASS_CAST((klass), \\
	{{ns_upper}}_TYPE_{{object_upper}}, {{class_camel}}Class))

#define {{ns_upper}}_IS_{{object_upper}}(obj) \\
	(G_TYPE_CHECK_INSTANCE_TYPE((obj), \\
	{{ns_upper}}_TYPE_{{object_upper}}))

#define {{ns_upper}}_IS_{{object_upper}}_CLASS(klass) \\
	(G_TYPE_CHECK_CLASS_TYPE((klass), \\
	{{ns_upper}}_TYPE_{{object_upper}}))

#define {{ns_upper}}_{{object_upper}}_GET_CLASS(obj) \\
	(G_TYPE_INSTANCE_GET_CLASS((obj), \\
	{{ns_upper}}_TYPE_{{object_upper}}, {{class_camel}}Class))

typedef struct _{{class_camel}} {{class_camel}};
typedef struct _{{class_camel}}Class {{class_camel}}Class;
{{#has_private}}
typedef struct _{{class_camel}}Private {{class_camel}}Private;
{{/has_private}}

struct _{{class_camel}}
{
	/*< private >*/
	{{parent_camel}} parent;

	{{#has_private}}
	{{class_camel}}Private *priv;
	{{/has_private}}
};

struct _{{class_camel}}Class
{
	/*< private >*/
	{{parent_camel}}Class parent_class;
};

GType {{class_lower}}_get_type(void) G_GNUC_CONST;

{{^is_abstract}}
{{class_camel}}* {{class_lower}}_new(void);
{{/is_abstract}}

G_END_DECLS

#endif /* {{header_guard}} */
"""

TEMPLATE_CLASS_CODE = """
#include "{{filename}}.h"

/**
 * SECTION:{{filename}}
 * @short_description:
 * @title: {{class_camel}}
 *
 * Insert documentation here.
 */

{{#ifaces}}
static void {{iface_lower}}_iface_init({{iface_camel}}Iface *iface);
{{/ifaces}}

/**
 * {{class_camel}}:
 *
 * Insert documentation here.
 */
{{^is_abstract}}
{{#implements_iface}}
G_DEFINE_TYPE_WITH_CODE({{class_camel}},
						{{class_lower}},
						{{parent_ns_upper}}_TYPE_{{parent_object_upper}},
						{{implemented_ifaces}})
{{/implements_iface}}
{{^implements_iface}}
G_DEFINE_TYPE({{class_camel}},
			  {{class_lower}},
			  {{parent_ns_upper}}_TYPE_{{parent_object_upper}})
{{/implements_iface}}
{{/is_abstract}}
{{#is_abstract}}
{{#implements_iface}}
G_DEFINE_ABSTRACT_TYPE_WITH_CODE({{class_camel}},
								 {{class_lower}},
								 {{parent_ns_upper}}_TYPE_{{parent_object_upper}},
								 {{implemented_ifaces}})
{{/implements_iface}}
{{^implements_iface}}
G_DEFINE_ABSTRACT_TYPE({{class_camel}},
					   {{class_lower}},
					   {{parent_ns_upper}}_TYPE_{{parent_object_upper}})
{{/implements_iface}}
{{/is_abstract}}

{{#has_private}}
#define {{object_upper}}_PRIVATE(o) \\
	(G_TYPE_INSTANCE_GET_PRIVATE((o), {{ns_upper}}_TYPE_{{object_upper}}, {{class_camel}}Private))

struct _{{class_camel}}Private
{
	void* __dummy;
};
{{/has_private}}

{{#ifaces}}
static void
{{iface_lower}}_iface_init({{iface_camel}}Iface *iface)
{
}
{{/ifaces}}

{{#has_propset}}
static void
{{class_lower}}_set_property(GObject *object, guint property_id, const GValue *value, GParamSpec *pspec)
{
	switch (property_id) {
	default:
		G_OBJECT_WARN_INVALID_PROPERTY_ID(object, property_id, pspec);
		break;
    }
}
{{/has_propset}}

{{#has_propget}}
static void
{{class_lower}}_get_property(GObject *object, guint property_id, GValue *value, GParamSpec *pspec)
{
	switch (property_id) {
	default:
		G_OBJECT_WARN_INVALID_PROPERTY_ID(object, property_id, pspec);
		break;
    }
}
{{/has_propget}}

{{#has_dispose}}
static void
{{class_lower}}_dispose(GObject *object)
{
	G_OBJECT_CLASS({{class_lower}}_parent_class)->dispose(object);
}
{{/has_dispose}}

{{#has_finalize}}
static void
{{class_lower}}_finalize(GObject *object)
{
	G_OBJECT_CLASS({{class_lower}}_parent_class)->finalize(object);
}
{{/has_finalize}}

{{#has_class_init}}
static void
{{class_lower}}_class_init({{class_camel}}Class *klass)
{
	GObjectClass *object_class = G_OBJECT_CLASS(klass);

	{{#has_private}}
	g_type_class_add_private(klass, sizeof({{class_camel}}Private));
	{{/has_private}}

	{{#has_propset}}
	object_class->set_property = {{class_lower}}_set_property;
	{{/has_propset}}
	{{#has_propget}}
	object_class->get_property = {{class_lower}}_get_property;
	{{/has_propget}}
	{{#has_dispose}}
	object_class->dispose = {{class_lower}}_dispose;
	{{/has_dispose}}
	{{#has_finalize}}
	object_class->finalize = {{class_lower}}_finalize;
	{{/has_finalize}}
}
{{/has_class_init}}

static void
{{class_lower}}_init({{class_camel}} *self)
{
	{{#has_private}}
	self->priv = {{object_upper}}_PRIVATE(self);
	{{/has_private}}
}

{{^is_abstract}}
/**
 * {{class_lower}}_new:
 *
 * Creates a new #{{class_camel}}.
 *
 * Returns: the newly created #{{class_camel}}.
 */
{{class_camel}}*
{{class_lower}}_new(void)
{
	return g_object_new({{ns_upper}}_TYPE_{{object_upper}}, NULL);
}
{{/is_abstract}}
"""

TEMPLATE_IFACE_DECL = "G _IMPLEMENT_INTERFACE(%(iface_ns_upper)s_TYPE_%(iface_name_upper)s, %(iface_lower)s_iface_init)"

TEMPLATE_IFACE_HEADER = """
#ifndef {{header_guard}}
#define {{header_guard}}

#include <glib-object.h>

G_BEGIN_DECLS

#define {{ns_upper}}_TYPE_{{iface_upper}} {{iface_lower}}_get_type()

#define {{ns_upper}}_{{iface_upper}}(obj) \\
	(G_TYPE_CHECK_INSTANCE_CAST((obj), \\
	{{ns_upper}}_TYPE_{{iface_upper}}, {{iface_camel}}))

#define {{ns_upper}}_IS_{{iface_upper}}(obj) \\
	(G_TYPE_CHECK_INSTANCE_TYPE((obj), \\
	{{ns_upper}}_TYPE_{{iface_upper}}))

#define {{ns_upper}}_{{iface_upper}}_GET_IFACE(obj) \\
	(G_TYPE_INSTANCE_GET_INTERFACE((obj), \\
	{{ns_upper}}_TYPE_{{iface_upper}}, {{iface_camel}}Iface))

typedef struct _{{iface_camel}} {{iface_camel}};
typedef struct _{{iface_camel}}Iface {{iface_camel}}Iface;

struct _{{iface_camel}}Iface
{
	/*< private >*/
	GTypeInterface g_iface;
};

GType {{iface_lower}}_get_type(void) G_GNUC_CONST;

G_END_DECLS

#endif /* {{header_guard}} */
"""

TEMPLATE_IFACE_CODE = """
#include "{{filename}}.h"

/**
 * SECTION:{{filename}}
 * @short_description:
 * @title: {{class_camel}}
 *
 * Insert documentation here.
 */
G_DEFINE_INTERFACE({{iface_camel}}, {{iface_lower}}, {{ns_upper}}_TYPE_{{iface_upper}})
"""