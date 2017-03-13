import SirTrevor from 'sir-trevor'
import Product from './product'
import Markup from './markup'


SirTrevor.Blocks.Product = SirTrevor.Block.extend(Product)
SirTrevor.Blocks.Markup = SirTrevor.Block.extend(Markup)

SirTrevor.setDefaults({
  uploadUrl: '/admin/images/image/st-upload/',
  ajaxOptions: {
    headers: {},
    credentials: 'same-origin'
  }
})

export default SirTrevor