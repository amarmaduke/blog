require 'execjs/fastnode'

module Jekyll
  module Tags
    class Katex < Liquid::Block

      KATEX_JS_PATH = './_js/katex.min.js'
      @@katex = ExecJS.compile(open(KATEX_JS_PATH).read)

      def initialize(tag_name, markup, tokens)
        super
        @tokens = tokens
        @markup = markup

        @display = markup.include? 'display'
      end

      def render(context)
        latex_source = super
        result = ''
        is_math = false
        i = 0
        while i < latex_source.length
          buffer = ''
          while i + 1 < latex_source.length && !(latex_source[i] == '$' && latex_source[i + 1] == '$')
            buffer = buffer + latex_source[i]
            i = i + 1
          end

          if i + 1 < latex_source.length
            i = i + 2
          else
            buffer = buffer + latex_source[i]
            i = i + 1
          end

          if is_math then
            result = result + @@katex.call("katex.renderToString", buffer, displayMode: @display)
          else
            result = result + buffer
          end

          is_math = !is_math
        end

        result
      end
    end
  end
end

Liquid::Template.register_tag('katex', Jekyll::Tags::Katex)