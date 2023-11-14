import struct
from pydantic import BaseModel


class Measurement(BaseModel):
    room_id: int
    device_id: int
    noise_value: int

    @classmethod
    def from_binary(cls, message: bytes):
        room_id, device_id, noise_value = struct.unpack("!IIi", message)
        return cls(
            room_id=room_id,
            device_id=device_id,
            noise_value=noise_value,
        )
