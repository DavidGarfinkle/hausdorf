// Code generated by protoc-gen-go. DO NOT EDIT.
// source: smr.proto

package proto

import (
	context "context"
	fmt "fmt"
	proto "github.com/golang/protobuf/proto"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	math "math"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion3 // please upgrade the proto package

type AddPieceRequest struct {
	Pid                  uint32   `protobuf:"varint,1,opt,name=pid,proto3" json:"pid,omitempty"`
	Notes                []*Note  `protobuf:"bytes,2,rep,name=notes,proto3" json:"notes,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *AddPieceRequest) Reset()         { *m = AddPieceRequest{} }
func (m *AddPieceRequest) String() string { return proto.CompactTextString(m) }
func (*AddPieceRequest) ProtoMessage()    {}
func (*AddPieceRequest) Descriptor() ([]byte, []int) {
	return fileDescriptor_3ce62a8635f91dac, []int{0}
}

func (m *AddPieceRequest) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_AddPieceRequest.Unmarshal(m, b)
}
func (m *AddPieceRequest) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_AddPieceRequest.Marshal(b, m, deterministic)
}
func (m *AddPieceRequest) XXX_Merge(src proto.Message) {
	xxx_messageInfo_AddPieceRequest.Merge(m, src)
}
func (m *AddPieceRequest) XXX_Size() int {
	return xxx_messageInfo_AddPieceRequest.Size(m)
}
func (m *AddPieceRequest) XXX_DiscardUnknown() {
	xxx_messageInfo_AddPieceRequest.DiscardUnknown(m)
}

var xxx_messageInfo_AddPieceRequest proto.InternalMessageInfo

func (m *AddPieceRequest) GetPid() uint32 {
	if m != nil {
		return m.Pid
	}
	return 0
}

func (m *AddPieceRequest) GetNotes() []*Note {
	if m != nil {
		return m.Notes
	}
	return nil
}

type AddPieceResponse struct {
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *AddPieceResponse) Reset()         { *m = AddPieceResponse{} }
func (m *AddPieceResponse) String() string { return proto.CompactTextString(m) }
func (*AddPieceResponse) ProtoMessage()    {}
func (*AddPieceResponse) Descriptor() ([]byte, []int) {
	return fileDescriptor_3ce62a8635f91dac, []int{1}
}

func (m *AddPieceResponse) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_AddPieceResponse.Unmarshal(m, b)
}
func (m *AddPieceResponse) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_AddPieceResponse.Marshal(b, m, deterministic)
}
func (m *AddPieceResponse) XXX_Merge(src proto.Message) {
	xxx_messageInfo_AddPieceResponse.Merge(m, src)
}
func (m *AddPieceResponse) XXX_Size() int {
	return xxx_messageInfo_AddPieceResponse.Size(m)
}
func (m *AddPieceResponse) XXX_DiscardUnknown() {
	xxx_messageInfo_AddPieceResponse.DiscardUnknown(m)
}

var xxx_messageInfo_AddPieceResponse proto.InternalMessageInfo

type GetPieceIdsRequest struct {
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *GetPieceIdsRequest) Reset()         { *m = GetPieceIdsRequest{} }
func (m *GetPieceIdsRequest) String() string { return proto.CompactTextString(m) }
func (*GetPieceIdsRequest) ProtoMessage()    {}
func (*GetPieceIdsRequest) Descriptor() ([]byte, []int) {
	return fileDescriptor_3ce62a8635f91dac, []int{2}
}

func (m *GetPieceIdsRequest) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_GetPieceIdsRequest.Unmarshal(m, b)
}
func (m *GetPieceIdsRequest) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_GetPieceIdsRequest.Marshal(b, m, deterministic)
}
func (m *GetPieceIdsRequest) XXX_Merge(src proto.Message) {
	xxx_messageInfo_GetPieceIdsRequest.Merge(m, src)
}
func (m *GetPieceIdsRequest) XXX_Size() int {
	return xxx_messageInfo_GetPieceIdsRequest.Size(m)
}
func (m *GetPieceIdsRequest) XXX_DiscardUnknown() {
	xxx_messageInfo_GetPieceIdsRequest.DiscardUnknown(m)
}

var xxx_messageInfo_GetPieceIdsRequest proto.InternalMessageInfo

type GetPieceIdsResponse struct {
	Pids                 []uint32 `protobuf:"varint,1,rep,packed,name=pids,proto3" json:"pids,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *GetPieceIdsResponse) Reset()         { *m = GetPieceIdsResponse{} }
func (m *GetPieceIdsResponse) String() string { return proto.CompactTextString(m) }
func (*GetPieceIdsResponse) ProtoMessage()    {}
func (*GetPieceIdsResponse) Descriptor() ([]byte, []int) {
	return fileDescriptor_3ce62a8635f91dac, []int{3}
}

func (m *GetPieceIdsResponse) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_GetPieceIdsResponse.Unmarshal(m, b)
}
func (m *GetPieceIdsResponse) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_GetPieceIdsResponse.Marshal(b, m, deterministic)
}
func (m *GetPieceIdsResponse) XXX_Merge(src proto.Message) {
	xxx_messageInfo_GetPieceIdsResponse.Merge(m, src)
}
func (m *GetPieceIdsResponse) XXX_Size() int {
	return xxx_messageInfo_GetPieceIdsResponse.Size(m)
}
func (m *GetPieceIdsResponse) XXX_DiscardUnknown() {
	xxx_messageInfo_GetPieceIdsResponse.DiscardUnknown(m)
}

var xxx_messageInfo_GetPieceIdsResponse proto.InternalMessageInfo

func (m *GetPieceIdsResponse) GetPids() []uint32 {
	if m != nil {
		return m.Pids
	}
	return nil
}

type SearchRequest struct {
	Notes                []*Note  `protobuf:"bytes,1,rep,name=notes,proto3" json:"notes,omitempty"`
	Pids                 []uint32 `protobuf:"varint,2,rep,packed,name=pids,proto3" json:"pids,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *SearchRequest) Reset()         { *m = SearchRequest{} }
func (m *SearchRequest) String() string { return proto.CompactTextString(m) }
func (*SearchRequest) ProtoMessage()    {}
func (*SearchRequest) Descriptor() ([]byte, []int) {
	return fileDescriptor_3ce62a8635f91dac, []int{4}
}

func (m *SearchRequest) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_SearchRequest.Unmarshal(m, b)
}
func (m *SearchRequest) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_SearchRequest.Marshal(b, m, deterministic)
}
func (m *SearchRequest) XXX_Merge(src proto.Message) {
	xxx_messageInfo_SearchRequest.Merge(m, src)
}
func (m *SearchRequest) XXX_Size() int {
	return xxx_messageInfo_SearchRequest.Size(m)
}
func (m *SearchRequest) XXX_DiscardUnknown() {
	xxx_messageInfo_SearchRequest.DiscardUnknown(m)
}

var xxx_messageInfo_SearchRequest proto.InternalMessageInfo

func (m *SearchRequest) GetNotes() []*Note {
	if m != nil {
		return m.Notes
	}
	return nil
}

func (m *SearchRequest) GetPids() []uint32 {
	if m != nil {
		return m.Pids
	}
	return nil
}

type SearchResponse struct {
	Occurrences          []*Occurrence `protobuf:"bytes,1,rep,name=occurrences,proto3" json:"occurrences,omitempty"`
	XXX_NoUnkeyedLiteral struct{}      `json:"-"`
	XXX_unrecognized     []byte        `json:"-"`
	XXX_sizecache        int32         `json:"-"`
}

func (m *SearchResponse) Reset()         { *m = SearchResponse{} }
func (m *SearchResponse) String() string { return proto.CompactTextString(m) }
func (*SearchResponse) ProtoMessage()    {}
func (*SearchResponse) Descriptor() ([]byte, []int) {
	return fileDescriptor_3ce62a8635f91dac, []int{5}
}

func (m *SearchResponse) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_SearchResponse.Unmarshal(m, b)
}
func (m *SearchResponse) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_SearchResponse.Marshal(b, m, deterministic)
}
func (m *SearchResponse) XXX_Merge(src proto.Message) {
	xxx_messageInfo_SearchResponse.Merge(m, src)
}
func (m *SearchResponse) XXX_Size() int {
	return xxx_messageInfo_SearchResponse.Size(m)
}
func (m *SearchResponse) XXX_DiscardUnknown() {
	xxx_messageInfo_SearchResponse.DiscardUnknown(m)
}

var xxx_messageInfo_SearchResponse proto.InternalMessageInfo

func (m *SearchResponse) GetOccurrences() []*Occurrence {
	if m != nil {
		return m.Occurrences
	}
	return nil
}

type Note struct {
	Onset                float32  `protobuf:"fixed32,1,opt,name=onset,proto3" json:"onset,omitempty"`
	Offset               float32  `protobuf:"fixed32,2,opt,name=offset,proto3" json:"offset,omitempty"`
	Pitch                int32    `protobuf:"varint,3,opt,name=pitch,proto3" json:"pitch,omitempty"`
	PieceIdx             uint32   `protobuf:"varint,4,opt,name=piece_idx,json=pieceIdx,proto3" json:"piece_idx,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *Note) Reset()         { *m = Note{} }
func (m *Note) String() string { return proto.CompactTextString(m) }
func (*Note) ProtoMessage()    {}
func (*Note) Descriptor() ([]byte, []int) {
	return fileDescriptor_3ce62a8635f91dac, []int{6}
}

func (m *Note) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Note.Unmarshal(m, b)
}
func (m *Note) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Note.Marshal(b, m, deterministic)
}
func (m *Note) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Note.Merge(m, src)
}
func (m *Note) XXX_Size() int {
	return xxx_messageInfo_Note.Size(m)
}
func (m *Note) XXX_DiscardUnknown() {
	xxx_messageInfo_Note.DiscardUnknown(m)
}

var xxx_messageInfo_Note proto.InternalMessageInfo

func (m *Note) GetOnset() float32 {
	if m != nil {
		return m.Onset
	}
	return 0
}

func (m *Note) GetOffset() float32 {
	if m != nil {
		return m.Offset
	}
	return 0
}

func (m *Note) GetPitch() int32 {
	if m != nil {
		return m.Pitch
	}
	return 0
}

func (m *Note) GetPieceIdx() uint32 {
	if m != nil {
		return m.PieceIdx
	}
	return 0
}

type Occurrence struct {
	Pid                  uint32   `protobuf:"varint,1,opt,name=pid,proto3" json:"pid,omitempty"`
	Notes                []*Note  `protobuf:"bytes,2,rep,name=notes,proto3" json:"notes,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *Occurrence) Reset()         { *m = Occurrence{} }
func (m *Occurrence) String() string { return proto.CompactTextString(m) }
func (*Occurrence) ProtoMessage()    {}
func (*Occurrence) Descriptor() ([]byte, []int) {
	return fileDescriptor_3ce62a8635f91dac, []int{7}
}

func (m *Occurrence) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Occurrence.Unmarshal(m, b)
}
func (m *Occurrence) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Occurrence.Marshal(b, m, deterministic)
}
func (m *Occurrence) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Occurrence.Merge(m, src)
}
func (m *Occurrence) XXX_Size() int {
	return xxx_messageInfo_Occurrence.Size(m)
}
func (m *Occurrence) XXX_DiscardUnknown() {
	xxx_messageInfo_Occurrence.DiscardUnknown(m)
}

var xxx_messageInfo_Occurrence proto.InternalMessageInfo

func (m *Occurrence) GetPid() uint32 {
	if m != nil {
		return m.Pid
	}
	return 0
}

func (m *Occurrence) GetNotes() []*Note {
	if m != nil {
		return m.Notes
	}
	return nil
}

func init() {
	proto.RegisterType((*AddPieceRequest)(nil), "proto.AddPieceRequest")
	proto.RegisterType((*AddPieceResponse)(nil), "proto.AddPieceResponse")
	proto.RegisterType((*GetPieceIdsRequest)(nil), "proto.GetPieceIdsRequest")
	proto.RegisterType((*GetPieceIdsResponse)(nil), "proto.GetPieceIdsResponse")
	proto.RegisterType((*SearchRequest)(nil), "proto.SearchRequest")
	proto.RegisterType((*SearchResponse)(nil), "proto.SearchResponse")
	proto.RegisterType((*Note)(nil), "proto.Note")
	proto.RegisterType((*Occurrence)(nil), "proto.Occurrence")
}

func init() { proto.RegisterFile("smr.proto", fileDescriptor_3ce62a8635f91dac) }

var fileDescriptor_3ce62a8635f91dac = []byte{
	// 337 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x9c, 0x92, 0x4d, 0x4f, 0xfa, 0x40,
	0x10, 0xc6, 0xd3, 0x96, 0x12, 0x98, 0x86, 0xff, 0x1f, 0x47, 0xc4, 0x5a, 0x2f, 0x75, 0x4f, 0xf5,
	0xc2, 0x01, 0xe2, 0xc9, 0x13, 0x89, 0x62, 0xbc, 0xa8, 0x59, 0x3e, 0x80, 0xd1, 0x76, 0x91, 0x1e,
	0x60, 0xd7, 0xee, 0x92, 0xf0, 0xed, 0xfc, 0x6a, 0x66, 0x5f, 0x28, 0x6f, 0x7a, 0xf1, 0xc4, 0xce,
	0x33, 0x0f, 0xbf, 0x9d, 0x3e, 0xb3, 0xd0, 0x96, 0x8b, 0x6a, 0x20, 0x2a, 0xae, 0x38, 0x86, 0xe6,
	0x87, 0x4c, 0xe0, 0xff, 0xb8, 0x28, 0x5e, 0x4a, 0x96, 0x33, 0xca, 0x3e, 0x57, 0x4c, 0x2a, 0xec,
	0x42, 0x20, 0xca, 0x22, 0xf6, 0x52, 0x2f, 0xeb, 0x50, 0x7d, 0xc4, 0x2b, 0x08, 0x97, 0x5c, 0x31,
	0x19, 0xfb, 0x69, 0x90, 0x45, 0xc3, 0xc8, 0x22, 0x06, 0x4f, 0x5c, 0x31, 0x6a, 0x3b, 0x04, 0xa1,
	0xbb, 0xe5, 0x48, 0xc1, 0x97, 0x92, 0x91, 0x1e, 0xe0, 0x03, 0x53, 0x46, 0x7b, 0x2c, 0xa4, 0xc3,
	0x93, 0x6b, 0x38, 0xdd, 0x53, 0xad, 0x19, 0x11, 0x1a, 0xa2, 0x2c, 0x64, 0xec, 0xa5, 0x41, 0xd6,
	0xa1, 0xe6, 0x4c, 0x26, 0xd0, 0x99, 0xb2, 0xb7, 0x2a, 0x9f, 0x6f, 0x46, 0xab, 0x07, 0xf1, 0x7e,
	0x1b, 0xa4, 0xe6, 0xf8, 0x3b, 0x9c, 0x7b, 0xf8, 0xb7, 0xe1, 0xb8, 0xdb, 0x46, 0x10, 0xf1, 0x3c,
	0x5f, 0x55, 0x15, 0x5b, 0xe6, 0x35, 0xee, 0xc4, 0xe1, 0x9e, 0xeb, 0x0e, 0xdd, 0x75, 0x91, 0x0f,
	0x68, 0xe8, 0x9b, 0xb0, 0x07, 0xa1, 0x86, 0x28, 0x13, 0x91, 0x4f, 0x6d, 0x81, 0x7d, 0x68, 0xf2,
	0xd9, 0x4c, 0xcb, 0xbe, 0x91, 0x5d, 0xa5, 0xdd, 0xa2, 0x54, 0xf9, 0x3c, 0x0e, 0x52, 0x2f, 0x0b,
	0xa9, 0x2d, 0xf0, 0x12, 0xda, 0x42, 0x47, 0xf0, 0x5a, 0x16, 0xeb, 0xb8, 0x61, 0xa2, 0x6e, 0x09,
	0x9b, 0xc9, 0x9a, 0x8c, 0x01, 0xb6, 0x33, 0xfc, 0x69, 0x1f, 0xc3, 0x2f, 0x0f, 0x82, 0xe9, 0xa2,
	0xc2, 0x1b, 0x68, 0xda, 0x4f, 0xc7, 0x9e, 0x73, 0xed, 0x25, 0x9a, 0x9c, 0x1d, 0xa8, 0x2e, 0x9f,
	0x5b, 0x68, 0x6d, 0xd6, 0x89, 0x7d, 0x67, 0x39, 0x78, 0x27, 0xc9, 0xf9, 0x91, 0xee, 0xfe, 0x7c,
	0x07, 0xd1, 0xce, 0x86, 0xf1, 0xc2, 0xf9, 0x8e, 0xdf, 0x42, 0x92, 0xfc, 0xd4, 0xb2, 0x94, 0xf7,
	0xa6, 0x69, 0x8d, 0xbe, 0x03, 0x00, 0x00, 0xff, 0xff, 0x2f, 0x7f, 0x08, 0x50, 0xb4, 0x02, 0x00,
	0x00,
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConn

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion4

// SmrClient is the client API for Smr service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type SmrClient interface {
	Search(ctx context.Context, in *SearchRequest, opts ...grpc.CallOption) (*SearchResponse, error)
	AddPiece(ctx context.Context, in *AddPieceRequest, opts ...grpc.CallOption) (*AddPieceResponse, error)
	GetPieceIds(ctx context.Context, in *GetPieceIdsRequest, opts ...grpc.CallOption) (*GetPieceIdsResponse, error)
}

type smrClient struct {
	cc *grpc.ClientConn
}

func NewSmrClient(cc *grpc.ClientConn) SmrClient {
	return &smrClient{cc}
}

func (c *smrClient) Search(ctx context.Context, in *SearchRequest, opts ...grpc.CallOption) (*SearchResponse, error) {
	out := new(SearchResponse)
	err := c.cc.Invoke(ctx, "/proto.Smr/Search", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *smrClient) AddPiece(ctx context.Context, in *AddPieceRequest, opts ...grpc.CallOption) (*AddPieceResponse, error) {
	out := new(AddPieceResponse)
	err := c.cc.Invoke(ctx, "/proto.Smr/AddPiece", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *smrClient) GetPieceIds(ctx context.Context, in *GetPieceIdsRequest, opts ...grpc.CallOption) (*GetPieceIdsResponse, error) {
	out := new(GetPieceIdsResponse)
	err := c.cc.Invoke(ctx, "/proto.Smr/GetPieceIds", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// SmrServer is the server API for Smr service.
type SmrServer interface {
	Search(context.Context, *SearchRequest) (*SearchResponse, error)
	AddPiece(context.Context, *AddPieceRequest) (*AddPieceResponse, error)
	GetPieceIds(context.Context, *GetPieceIdsRequest) (*GetPieceIdsResponse, error)
}

// UnimplementedSmrServer can be embedded to have forward compatible implementations.
type UnimplementedSmrServer struct {
}

func (*UnimplementedSmrServer) Search(ctx context.Context, req *SearchRequest) (*SearchResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Search not implemented")
}
func (*UnimplementedSmrServer) AddPiece(ctx context.Context, req *AddPieceRequest) (*AddPieceResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method AddPiece not implemented")
}
func (*UnimplementedSmrServer) GetPieceIds(ctx context.Context, req *GetPieceIdsRequest) (*GetPieceIdsResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetPieceIds not implemented")
}

func RegisterSmrServer(s *grpc.Server, srv SmrServer) {
	s.RegisterService(&_Smr_serviceDesc, srv)
}

func _Smr_Search_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SearchRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SmrServer).Search(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/proto.Smr/Search",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SmrServer).Search(ctx, req.(*SearchRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Smr_AddPiece_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(AddPieceRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SmrServer).AddPiece(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/proto.Smr/AddPiece",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SmrServer).AddPiece(ctx, req.(*AddPieceRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Smr_GetPieceIds_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GetPieceIdsRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(SmrServer).GetPieceIds(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/proto.Smr/GetPieceIds",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(SmrServer).GetPieceIds(ctx, req.(*GetPieceIdsRequest))
	}
	return interceptor(ctx, in, info, handler)
}

var _Smr_serviceDesc = grpc.ServiceDesc{
	ServiceName: "proto.Smr",
	HandlerType: (*SmrServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "Search",
			Handler:    _Smr_Search_Handler,
		},
		{
			MethodName: "AddPiece",
			Handler:    _Smr_AddPiece_Handler,
		},
		{
			MethodName: "GetPieceIds",
			Handler:    _Smr_GetPieceIds_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "smr.proto",
}
