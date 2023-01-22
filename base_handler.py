import sys
import http_req, http_resp


class Handler:
    async def handle_connection(self, reader, writer):
        print("new connection")
        try:
            await self.handle_http_req(reader, writer)
            writer.close()
            print("connection closed")
            await reader.wait_closed()
            print("connection finished")
        except EOFError:
            print("eof")

    async def handle_http_req(self, reader, writer):
        request = await http_req.read_request(reader)
        print(request.method, request.path)
        try:
            response = self.get_response(request)
        except Exception as exc:
            sys.print_exception(exc)
            response = http_resp.HttpResponse(
                status=500,
                headers={},
                content=b"",
                )
        print(response.status)
        http_resp.send_response(response, writer)

    def get_response(self, request):
        raise Exception("Not Implemented")