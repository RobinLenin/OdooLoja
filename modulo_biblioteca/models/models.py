from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Libro(models.Model):
    _name = "bi.libro"
    _description = "Libros"

    _sql_constraints = [
        ('name_unique', 'unique (name)', "Tag name already exists !"),
    ]

    #Campos básicos

    name = fields.Char(string = "Nombre del Libro", required= True)
    description = fields.Text(string="Descripcion del Libro")
    prestado = fields.Boolean(string = "Prestado", required= True, default = False)
    precio = fields.Float(string= "Precio del libro")

    descuento = fields.Float(string="Descuento")
    precio_des = fields.Float(string="Precio con Descuento", compute="calcular_descuento")
    cantidad = fields.Integer(string = "Cantidad de libros")
    #campos Avanzados
    libro_digital = fields.Binary(string= "Cargar Libro")
    resumen = fields.Html(string="Resumen")
    portada = fields.Image(string= "Cargar portada")
    categoria = fields.Selection([('literatura','Cat. Literatura'), ('matematica','Cat. Matemáticas'),
                                  ('soft','Cat. Software')])
    fecha_publicacion = fields.Date(string = "Fecha de Publicación")
    hora_publicacion = fields.Datetime(string="Hora de Publicación")

    #Campos relacionales

    user_id = fields.Many2one("res.user", string="Alquilado a", ondelete="cascade", default=lambda self: self.env.uid)

    categoria_ids = fields.Many2many(
        'bi.categoria', 'libro_categoria_rel',
        'categoria_id', 'libro_id', string="Categorias")



    def crear_registro(self):
        pass

    @api.depends("descuento", "precio")
    def calcular_descuento(self):
        for libro in self:
            aux = (libro.precio * libro.descuento)/100
            libro.precio_des = libro.precio - aux

    @api.onchange("descuento")
    def validar_descuento(self):
        if self.descuento < 0 or self.descuento > 100:
            #self.env.user.notify_info(message="Prueba")
            raise ValidationError("El descuento debe estar entre 0 - 100.")

    @api.model
    def create(self, vals):
        #>=, <=, =, !=, in
        libro = self.env["bi.libro"].search([('cantidad', '>', 33), ('precio', '>', 100)], limit=1)

        self.env['bi.libro'].browse(libro.id).write({"descuento": 30})

        self.env.cr.commit()


        nombre = vals.get('name')
        aux = "LI_"+nombre
        aux1 ="das"
        for libro in libro:
            print(libro.name)
            if libro.name == aux1:
                raise ValidationError("El nombre se repite")

        #vals.update({'name': aux})
        return super(Libro, self).create(vals)

    def write(self, values):
        print(self.cantidad)
        values['cantidad'] = -1
        return super(Libro, self).write(values)

    def unlink(self):
        for libro in self:
            if libro.cantidad > 0:
                raise ValidationError("No puedes eliminar un libro que tiene stock")

        return super(Libro, self).unlink()


    @api.constrains('fecha_publicacion')
    def validad_fecha_pu(self):
        hoy = fields.Date.today()
        if self.fecha_publicacion > hoy:
            raise ValidationError("La fecha de puclicación no puede sar mayor a hoy")


    def validar(self):
        libros = self.env["bi.libro"].search([('cantidad', '<', 5)])
        print("Libros que tienes <5 stock")
        for libro in libros:
            print(libro.name)

class ResUser(models.Model):
    _inherit = "res.users"

    libro_ids = fields.One2many("bi.libro", "user_id", ondelete="cascade")


class Categoria(models.Model):
    _name = "bi.categoria"
    _description = "Categorias"

    name = fields.Char(string="Categoria del Libro", required=True)
    description = fields.Text(string="Descripcion del Libro")











